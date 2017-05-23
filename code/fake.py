
def check_domain(domain):
    import re
    pref = re.compile(r'http[s]*://')
    d = re.sub(r'http[s]*://', '', domain)
    print d
    regexp = re.compile(r'[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*')
    if regexp.match(d):
        return d
    return ""

# spark_handler is the starting point of our application.  Pipeline calls this function and executes
# whenever your bot is called.  
def spark_handler(post_data, message):
    # get the room id: 
    room_id = post_data["data"]["roomId"]

    # Paste in your Umbrella Security Token here: 
    token = 'YOUR UMBRELLA SECURITY TOKEN'

    # Get the last value and see if its fake news. 
    d = message.text.split(" ")[-1] 
    d = check_domain(d)
    if d != "":
        spark.messages.create(roomId=room_id, text="Checking on domain: " + d + "...")
        spark.messages.create(roomId=room_id, text=check_fake_news(token, message.text.split(" ")[-1]))
    else: 
        spark.messages.create(roomId=room_id, text="Please give me a domain to see if its fake news!")
        

# get our database of fake news sites.
def fakenews_get():
    from urllib2 import Request, urlopen, HTTPError
    header = { 'Content-Type': 'application/json' }
    url = "https://raw.githubusercontent.com/vallard/fakenewsbot/master/fakesites.json"
    req = Request(url, headers=header)
    try:
        fh = urlopen(req)
    except HTTPError, e:
        print "Error getting fake news sites: " + e.code
        return []
    out = json.loads(fh.read())
    return out["domains"]

# umbrella_get performs a get operation against the investigate API
# pass in the umbrella token and the path to the API you wish to call. 
# See the API documentation for examples of paths: 
# https://docs.umbrella.com/developer/investigate-api/
def umbrella_get(token, path):
    from urllib2 import Request, urlopen, HTTPError
    headers = {  'Authorization': 'Bearer ' + token }
    url = 'https://investigate.api.opendns.com' + path
    req = Request(url, headers=headers)
    try:
        fh = urlopen(req)
    except HTTPError, e:
        if e.code == 403:
            return False, "error authenticating with investigate API. Bot creater didn't enter token correctly?"
        elif e.code == 404:
            return False, url + " doesn't seem to exist."
    return True, json.loads(fh.read())

# get all kinds of security info for this domain.  So much!
# https://docs.umbrella.com/developer/investigate-api/security-information-for-a-domain-1/
def get_security_info(token, domain):
    ok, response = umbrella_get(token, "/security/name/" + domain +  ".json")
    return ok, response

# get_domain_score
# https://docs.umbrella.com/developer/investigate-api/domain-scores-1/
def get_domain_score(token, domain):
    ok, response =  umbrella_get(token, "/domains/score/" + domain + "?showLabels")
    return ok, response


# get_domain_categories gets categorization of the domain. 
# https://docs.umbrella.com/developer/investigate-api/domain-status-and-categorization-1/
def get_domain_categories(token, domain):
    ok, response =  umbrella_get(token, "/domains/categorization/" + domain + "?showLabels")
    return ok, response

# get_domain_whois gets the whois information from investigate
# https://docs.umbrella.com/developer/investigate-api/whois-information-for-a-domain-1/    
def get_domain_whois(token, domain):
    ok, response =  umbrella_get(token, "/whois/" + domain)
    return ok, response
   
# get_domains_by_email gets emails from users given an email and token 
# https://docs.umbrella.com/developer/investigate-api/whois-information-for-a-domain-1/
def get_domains_by_email(token, email):
    ok, response =  umbrella_get(token, "/whois/emails/" + email)
    return ok, response



# below we gather scores by parsing the data from the investigate primatives. 
def score_from_categories(token, domain):
    ok, response = get_domain_categories(token, domain)
    if not ok:
        return ok, response

    categories =  response[domain]["security_categories"]
    for c in categories:
        if c == "Malware" or c == "Phishing" or c == "Botnet" or c == "Suspicious":
            return ok, 50        
    return ok, 0

# check the time and see if it was created less than a year ago.  If it was
# return 20.  If it wasn't, then return 0. 
def when_created_score(created): 
    from datetime import datetime
    created_date = datetime.now()
    if created != None:
        created_date = datetime.strptime(created, '%Y-%m-%d')
    present = datetime.now()
    time_delta = present - created_date
    if time_delta.days < 365:
        return 20
    return 0

# see if domain is related to other bad domains. 
def score_from_database(domains):
    bad_domains = fakenews_get()
    for domain in domains:
        if domain in bad_domains:
            return 50
    return 0

# check_number_of_emails calls get_domains_by_email then returns the count 
def score_from_whois(token, domain):
    who_score = 0
    ok, whois_info = get_domain_whois(token, domain)
    if not ok:
        return ok, whois_info


    emails = whois_info["emails"]
    # just check the first email..
    email = emails[0]
    ok, r = get_domains_by_email(token, email)
    if not ok:
        return ok, r

    if len(r[email]["domains"]) == 1:
        who_score += 50
    # check other scores. 
    who_score += score_from_database(r[email]["domains"])
        
    # check if created time 
    who_score += when_created_score(whois_info["created"])
    return ok, who_score
  
def score_from_security(token, domain):
    score = 0
    ok, sec_info = get_security_info(token, domain)
    if not ok:
        return ok, sec_info

    page_rank = sec_info['pagerank']
    if page_rank < 3:
        return ok, 10
    return ok, 0
    

 
# check_fake_news takes API token and a website.  The algorithm is pretty
# crude and can be modified by you.  
def check_fake_news(token, domain):
    score = 0
    # goet score from categories
    ok, s = score_from_categories(token, domain)
    if not ok:
        return s
    score += s
    
    # get domain share score
    ok, s = score_from_whois(token, domain)
    if not ok:
        return s
    score += s

    # figure out security page score. 
    ok, s = score_from_security(token, domain)
    if not ok:
        return s
    score += s
 
    msg = "" 
    if score >= 99:
        msg = "%s has a greater than %99 probability of being fake news" % domain
    else:
        msg  = "%s has a %%%.2f probability of being a fake news site" % (domain, ((float(score) / float(100)) * 100))
    return msg

## for testing, not required for code. 
import sys 
import json
import os
token = os.environ.get('UMBRELLA_TOKEN')
if token == None:
    print "please define UMBRELLA_TOKEN environment variable"
    sys.exit(1)
if len(sys.argv) > 1:
    domain = check_domain(sys.argv[1])
    if domain != "":
        print check_fake_news(token, domain)
else:
    print "Please call this program with a domain"
