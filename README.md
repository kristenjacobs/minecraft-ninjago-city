# Minecraft Ninjago City

The brief from my 7 year old was to produce Ninjago City in Mincraft.
With that in mind, here's an example of using Python to generate structures
in Minecraft. Looks nothing like Ninjago city (although I'm not sure what it should
look like..), but was fun all the same.

## Setup

* Make sure you have the PC edition (I'm using it on Linux).

* Install Minecraft forge (This manages Minecraft mods).
See: https://unix.stackexchange.com/questions/293425/how-do-i-install-minecraft-forge

* Install the Minecraft mod that enables the Python scripting.
See: https://github.com/arpruss/raspberryjammod
and http://www.instructables.com/id/Python-coding-for-Minecraft

## Install 

```
cp ninjago_city.py ~/.minecraft/mcpipy/
```

## Run

Start mincraft, create a new flat world with no structures, then 
from inside minecraft type

```
/py ninjago_city.py
```

Step back and enjoy!

![Ninjago City 1](/images/ninjago-city-1.png)
![Ninjago City 2](/images/ninjago-city-2.png)
