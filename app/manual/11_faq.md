Project Management {#project_management}
=======================

*	[Where should I start?](@ref start)
*   [What are the levels?](@ref levels)
*   [Why so many levels?](@ref why_levels)
*   [Is NAP difficult?](@ref difficulty)

# Where should I start? {#start}

If you're completely new to NAP it's best to [download](https://github.com/napframework/nap/releases) the pre-compiled `packaged framework` and try out some of the demos. Start with `helloworld` demo and work your way up in difficulty. All demos are well documented and explain various core concepts, including their building blocks. 

If you like what you see and want to get down and dirty with NAP application development, then it's better to directly work against [source](https://github.com/napframework/nap) as we (the authors) do. This allows you to develop against the NAP source code; which is useful if you want to understand the various bits and pieces that make everything tick! 

Contrary to what you might think, compiling and working with NAP from source is relatively straight forward and doesn't involve a lot of custom setup, compared to the framework release. The steps are explained in the online [.readme](https://github.com/napframework/nap?tab=readme-ov-file#compilation), which boil down to: Clone NAP, download and extract pre-compiled Qt, setup the `QT_DIR` environment variable, run the setup script and generate the solution. It won't take more than 10 minutes on most supported platforms, why? Because almost all third party are pre-compiled and should work out of the box.

# What are the various levels? {#levels}

NAP has 3 distinct levels:

1: NAP from Source; framework source code
2: NAP from Package; compiled framework package
3: NAP App; compiled distributable application

# Why so many levels? {#why_levels}

Good question! Having a pre-compiled binary release of the framework allows you to freeze and create a `snapshot` of the entire framework your application is developed against, which turns out to be very convenient when you least expect it! 

As we know, software is always in a state of flux and maybe broken, unsupported or different 1, 2 or 5 years from now. Having a complete snapshot of the entire NAP stack helps you get back in when you don't want to; without having to gather all the various bits and pieces that are maybe no longer available, unsupported or broken. This becomes especially important when you are responsible for many projects, at many different locations on operating systems and versions. 

It is also an easy way to share the project with other developers, without the need to provide them with access to all your modules, branches and other changes; parts of which might be private.

# Is NAP difficult? {#difficulty}

Yes, in the beginning, until it clicks. If it doesn't click for you that's ok, don't beat yourself up over it! Some people like it, others don't. 

With that out of the way; C++ already isn't the easiest language and concepts like RTTI, which are essential to how the editor and framework operate, can be especially challenging if you're new to these ideas. But once you grasp them, you’ll be rewarded with unmatched flexibility, speed, and modularity; transforming your intricate ideas into powerful tools or instruments.

And then there’s Vulkan: yes, it’s infamous for requiring hundreds of lines of code just to render a triangle. But here’s the good news; you don’t have to write all that code yourself. We’ve built a complete engine from scratch so you can start creating impressive visuals right away. In NAP, you won’t need to touch Vulkan unless you want to (and you really should—it’s incredible).

If you find the code challenging, we strongly suggest reading Effective Modern C++ by Scott Meyers. The book clearly explains the many new concepts of modern C++ that we use everywhere in NAP.

If you struggle with the code, we highly recommend reading [Effective Modern C++](https://www.oreilly.com/library/view/effective-modern-c/9781491908419/) by Scott Meyers. The book clearly explains the many new concepts of modern C++ that we use everywhere in NAP.

# Where is 


