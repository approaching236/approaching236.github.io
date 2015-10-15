---
layout: post
title:  "Using an activerecord enum with simpleform"
date:   2015-10-15 13:00:00
categories:
---

I was having some trouble using an activerecord enum with simpleform, so I wanted to share my solution.

I have this concept on an exclusion, which is just another object like normal, but I wanted to validate against a certain field in a different object.

I wanted to be able to access the enum list elsewhere otherwise I would have just dropped the array into the enum section.
Just to save you a headache, make sure you only ever add to the back of this when you make updates, or use the hash format that I've seen lying around otherwise you are going to ruin your day when your database suddenly becomes incompatable with your code.
{% highlight ruby %}
# app/models/exclusion.rb

class Exclusion < ActiveRecord::Base
  ALLOWABLE_FIELDS = [:artist, :venue_name]

  enum field: ALLOWABLE_FIELDS
  validates :excluded_string, :field, :username, :reasoning, presence: true
end
{% endhighlight %}

Not too strange, but the enum field actually needs to be an integer. Some activerecord and simple form magic will make this work, no worries.
{% highlight ruby %}
# segment from db/schema.rb

create_table "exclusions", force: true do |t|
  t.string   "excluded_string"
  t.integer  "field" # totes an integer
  t.datetime "created_at"
  t.datetime "updated_at"
  t.string   "username"
  t.text     "reasoning"
end
{% endhighlight %}

Back out in the view, we just need to tell simpleform to use the collection.
It seems to automagically transpose the array of symbols into strings, then back to integers when it comes to throwing it back into the db.
Notice that the collection that is used is that constant symbol array that I made.
{% highlight erb %}
<%# app/views/exclusions/_form.html.erb %>

<%= simple_form_for(@exclusion) do |f| %>
  <%= f.error_notification %>

  <div class="form-inputs">
    <%= f.input :excluded_string %>
    <%= f.input :field, collection: Exclusion::ALLOWABLE_FIELDS %>
    <%= f.input :username %>
    <%= f.input :reasoning %>
  </div>

  <div class="form-actions">
    <%= f.button :submit %>
  </div>
<% end %>
{% endhighlight %}

And there we have it, no special gems required.
