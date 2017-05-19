# Example Walkthrough

Now, lets examine a detailed walkthrough of an example domain to see how this may work. In this exercise, we provided some arbitrary values for different elements that help one determine if a domain is serving fake news. It is really up to you to completely add upon this using your ingenuity and creativity!

As reading this, be thinking how you could make use of this information to customize and improve the accuracy of your bot. Complete documentation can be found at [http://docs.umbrella.com](http://docs.umbrella.com).


As an example, let's use the domain http://cnn.com.de/

Upon navigating to this site, you might believe it is CNN
<img src="images/cnn_com_de.png">

Does it have a convincing logo?

Let's look up this domain in [Umbrella Investigate](http://investigate.umbrella.com). <p>

### Domain Search
Once logged in, simply type the name of the domain in the search bar.
<img src="images/cnn_com_de_search.png">


### Security Information/Traffic
From here, we can see some information about the domain. This includes information like is it on Umbrella's block list because it is associated with a botnet, malware, C&C, etc. <p>
<img src="images/g_docs_pro.png"> <p>

We can also see some indication of this domain's traffic (based on the [100B+ requests](https://system.opendns.com) that Umbrella has visibility into globally). In this case, this was one of the domains affiliated with the [Google Docs phishing attack](https://umbrella.cisco.com/blog/2017/05/04/detecting-google-docs-phishing-attack-using-traffic-analysis/) a few weeks ago. <p>

### Whois
A little further down the page, we can see some information available from whois. This information will vary depending on the registrar used for the domain. <p>
<img src="images/cnn_com_de_whois.png"> <p>

There is some interesting information we can gleam from here including:<p>

 * When was this domain registered? A very recently registered domain may be an indication that the domain isn't a trusted news source that has been around for a while.
 * The e-mail address of who registered the domain? Does this look like a legitimate e-mail address? Should a personal e-mail address be used for a legitimate news site? Would a legitimate news site use a proxy anonymizer address?
 * How many other domains did this user register? Click the e-mail address to find out!
 * What nameservers are being used for the domain? ns1.superofficialnews.com looks a bit interesting doesn't it!

 For example, here are some other e-mails that are associated with this same e-mail address. Notice some other domains related to known legitimate news sites. <p>
 <img src="images/associated_domains.png">

### Associated Samples

The associated samples displays SHA256 signatures of malicious content that has been found to be associated with the domain/IP in question. Furthermore, this includes integration with Cisco AMP Threat Grid so you can drill into ThreatGrid in a single click.
<img src="images/associated_samples.png">

### Domain Tagging

This section displays a history of the domain's security status over the course of time. This can be useful to see if a site was previously flagged as malicious and later removed from the block list.
<img src="images/domain_tagging.png">

### Features
The features section displays some other important information regarding the domain. This includes things like:

 * TTL (time to live) for the domain
 * country codes
 * Associated ASNs
 * whether a mail exchanger exist for the domain. Would a legitimate news site have mail for its domain?

<img src="images/features.png">
Hover over each category to read more information about it. How might you incorporate this info into your bot?

### Security Features
This section contains more security related information about the domain. This includes some items like SecureRank based on how suspicious the domain may be and its PageRank (according to Google).
The requester geo distribution shows where the users are visiting the domain from? Would you suspect a US news site to have the majority of its visitors from Russia?
<img src="images/security_features.png">

### DGA Detection
DGA stands for domain generation algorithm and this score includes how likely a domain might have been automatically generated. The screen shot below is for the domain dqtfhkgskushlum[.]org
<img src="images/dga.png">

### IP Addresses and Name Servers
These sections are self-explanatory.

### Co-occerances
This section shows other domains that were called at around the same time (+- a few seconds) from the domain you are investigating. Often times, a site will be targeted for exploit and only serve up malware to an unsuspecting user who is on a platform that the malware can exploit. This can be useful in determining why a domain was called in the first place. <p>
<img src="images/co-occurences.png">

















