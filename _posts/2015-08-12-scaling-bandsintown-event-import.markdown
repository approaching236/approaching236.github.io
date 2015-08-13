---
layout: post
title:  "Scaling Bandsintown Event Import"
date:   2015-08-12 15:08:49
categories: 
---

Bandsintown is a company that helps people go to live shows by presenting them with shows that they might be interested in going to. This post is about some troubles that I tracked down between the event aggregation and import components of our backend wherein I got a chance to optimize a very important part of our infrastructure. My role at the company centers around getting event information into our system and available to our users. I want to present my work with bottlenecks like this. There isn't anything ground breaking here but this is a good example of how to shore up existing processes while sensibly balancing these strategies.

* Parallelism
* More horsepower
* Code optimization
* Third party services

I have a small cluster of applications, but relevant to this post are two primary components.

The first in the chain is the event collection application. It is a bunch of web scrapers all on a shared platform that can find event data on a number of different venue, ticket, artist and other websites. I'd like to get into that system in another post, but at one point that system had an internal cache that would limit the number of events sent to import.

The other component is the main monolithic Rails app that does pretty much anything at the company involving a database. This application needs to get split up a bit in my opinion. It does a lot of really unrelated stuff, but hey, 2007 was a heady time for the Rails community. In the spirit of hopefully someday splitting the import pipeline into it's own application we have a whole server propped up that does nothing but event import even though it's a complete copy of our monolith.

Now what we have isolated from the rest of our infrastructure seems to me to be a fairly common pattern. Something something university producer/consumer. Being the good office drones that our contractors and myself are, we got that producer producing something productive, up from about 100k events per day to over 360k. Granted, much of this information is duplicative. Between each batch, between the ticket sources that we are interested in, between what we already have imported, etc. Really there are some thousands of new events per day. 

This interface between collection and import went through a number of iterations worth talking about.

What existed when I started was a system of scp and sshing into the import machine to run import scripts at the end of each scrape of a website. I even found a chron job on the collection application that basically ran garbage collection on the remote. Janky as this might seem to me, it did the job sort of. It moved the files over successfully, it invoked the import script and got the events to our users. It did fail at some sort of important things. Logging whether it worked or not. Not dropping large numbers of events. A complete inability to run again if something failed. I honestly probably could have massaged this into something viable but I have come to a strong appreciation for a well made api and the benefits that one can provide to either side of the interface by having a contract.

So I made an endpoint on the import server that was a wrapper around the old scheme but with the event data in the post body of the HTTP request. So we would kick off a bunch of scrapers, each scraper would get events, then hit this endpoint with it's big batch of events, be told that they were imported and finish. This already worked swimmingly if it weren't for the fact that our scrapers can produce a lot of data. We started to get timeouts on large imports. It was kind of random at first, not all scrapers produce data that import at the same speed. Some require more comparisons than others. The import process took too long to run synchronously with the HTTP connection open so this got pushed into a background job. This upped the limit to a larger number, but it still didn't work with all the data sources that we wanted to be able to import so we had to consider some options for getting some files in the range of a few MB over to the import server.

* scp -- This would get the data over no problem. Where it goes, how to resolve conflicts, how to delete the files when they weren't needed were all solved problems that would need some configuration at most. This felt like it was breaking the idea of an API. It circumvented the interface to do it's own thing, then used the interface after the fact.
* batch import -- We could break the import down into many pieces. Say 1000 events per batch, each batch feeding into an overall import for a data source. We already had so many moving parts it seemed silly to introduce a whole new object into the collection side to manage if all parts had been imported successfully or not, not to mention all of the machinery required to synchronize them for a coherent report. Honestly just seemed like more trouble than it was worth.
* devops -- This request has no requirement for time. As far as I care, the connection could stay open for 10 minutes while it uploads. I'm a little fuzzy on why I discredited this one exactly, but I'm pretty sure it had to do with devops not being terribly fond of me having outlandish requirements for their nginx config.
* s3 -- Upload the file to s3, provide the url in the POST. This decision afforded me many benefits in the future that I hadn't predicted. Turns out it's really handy to have historical data available that you can pass around by url. This turned out to be really easy with the gems that are available for s3 as well. Invalidation is also handled by the api, so we don't end up paying for more than we need. We don't have a large number requirements for this information to be public, so if this method has cons, it's that we are paying for a service that could be in-housed.

That leaves us in a good state. Now there is a well defined interface that accepts a url to the event data and some other metadata. That endpoint returns if the background job was created correctly and information about that job. The background job then downloads that data, parses it, then hits a callback that was provided in the initial request to flag that the event data is available for that data source.


{% highlight ruby %}
def print_hi(name)
  puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}
