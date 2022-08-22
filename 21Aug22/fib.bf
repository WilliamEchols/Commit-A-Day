A program written in brainf*** (an esoteric language) that outputs the fibonnaci sequence (until it overflows when the sequence reaches double digits) using only four memory cells in total 
In order to preserve the authenticity of the development process, this singular file contains both the condensed and commented versions of the code

CONDENSED:-[----->+<]>---.<-[----->>+<<]>>--<[[-<+>>>+<<]>[-<+>]>[-<<+>>]<<>-[----->+<]>---[-<<->>]<<.<[->>+<<]>]

COMMENTED:

INIT
0-[----->+<]>---.
1<-[----->>+<<]>>--<

ADD LOOP
[
duplicate[-<+>>>+<<]
sum p1 >[-<+>]
sum p2 >[-<<+>>]<<
ASCII48 >-[----->+<]>---delete[-<<->>]<<.
reposition <[->>+<<]>
]