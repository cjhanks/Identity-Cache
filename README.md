# Using Cache TTL's to Track Sessions

## What Does it Do?

Browsers typically obey the cache, even in Incognito mode.  While there is a 
cache barrier between Public and Private browsing, there appears to be no 
barrier between tabs/windows in a private browsing session.

There are *other* uses for this sort of TTL caching.

It also allows for a session to be tracked even when a browser is using a VPN,
even if that VPN uses many IP addresses.  It can help in associating activity
of portable electronics using wireless networks.

Additionally, this works even when the browser has disabled JavaScript.


## Why Do I Want This?

You probably don't.  If you have a small server which is only expected to have
very constrained web-browser activity, this *can* help in associating different
masked activities by a single (or small number of users) to your site.

If you have a high-traffic site, this sort of implementation results in 
overloaded TCP connection queues.  Though `HTTP2` may improve things, it is 
still very wasteful.  There are possibly asynchronous alternatives in the 
JavaScript world.


## How Does it Do it?

It's not very sophisticated.  It places 10 CSS links, to support a system of
2 control bits and 8 data bits.  The control links are the `head` and the 
`tail`.

### The `/sentinal/head`

This has a maximum TTL and will only be fetched the first time visits the 
site.  This informs the internal system that a new identity is being crated,
it selects an arbitrary identity and informs them of the IP address that is
constructing the identity.  This is obviously not *perfect*, but it works
well enough for this demonstration.

### The `/sentinal/id`

When creating a new ID, as is the case when `/sentinal/head` was called, 
this is responsible for setting the initial cache logic.  If there is no 
new entitity being created already, then this is a bit mask value.

### The `/sentinal/tail`

This is a never-cached endpoint.  It is as a simple "closure" of the 
bit-cache stream and is not truly necessary for non real-time monitoring.

In the event that it was a new ID, it simply prints the new ID.  In the 
event that it was an existing ID, it prints the bitmask of the visited
sentinal subdirectories.

