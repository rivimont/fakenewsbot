# Algorithm

Below is a demonstration of how the algorithm will work. Remember, this is completely customizable and the idea is to just provide some ideas to get you started! Be creative!

The workflow is that you go to a news site and then to analyze that web site you pass the domain to the bot you are creating.

The most critical factors in determining a sites fakeness are at the top and as such weighted more heavily. You start with a score of 0 and if elements tie the domain to fake news, the score increases. At the end of the calculations, if the score is above X then there is a strong chance the domain is fake.

to start, **score** = 0

domain.com
<br>▼ <br>
Is the domain associated with a known security category (malware, phishing, botnet)? <br>
if yes, **score=score+50**
<br> ▼ <br>
Does the domain share a name server (or registration e-mail) with known fake news sites?
<br>if yes, **score=score+50**
<br> ▼ <br>
How many domains are tied to the owner's e-mail address?
<br> if 1 (strong chance of a proxy), **score=score+30**
<br> ▼ <br>
When was the domain registered?
<br> if in the last year, **score=score+20**
<br> ▼ <br>
How popular is the site?
<br>if pagerank less than 3, **score=score+10**
<br> ▼ <br>
Is there a mail exchanger associated with the domain?
<br> if no, **score=score+8**
<br> ▼ <br>
If final score > 15 then highly likely the site is fake

Now we will run through an example...




    