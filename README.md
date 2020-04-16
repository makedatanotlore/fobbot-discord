# Fobbot, the Forbidden Lands Dice Bot

## Features
* Dice in the same colors as the official dice
* English and Swedish support
* Regular D6s for when you need to roll a D66 or similar (or add -an to your command for actual numbers rolled)
* Push your roll by clicking a reaction "button" (within 10 minutes)
* Dwarves can push up to 10 times (the player rolling needs a Discord role called `dwarf` or `dvärg`)
* Resource dice
* Negative bonus dice

### [Add Fobbot to your own server](https://discordapp.com/api/oauth2/authorize?client_id=545345647390490640&permissions=288832&scope=bot)

## Contact
Connect to the [makedatanotlore Discord server](https://discord.gg/BSxpaQP) if you need to get in touch. 

## How to Roll
To roll dice, enter the number of dice followed by the type. Click 🔄 to push. Use `>help` to 

### Example Usage
`>roll 5ba 2sk 2gr d8`

*Remember to smash that space button.*

### Regular Dice Types
* Base Attribute Die - `ba`
* Skill Die - `sk`
* Gear/Weapon Die - `gr/wp`
* Artifact Die D8 - `d8`
* Artifact Die D10 - `d10`
* Artifact Die D12 - `d12`

### Resource Dice
For when you need to use a resource such as food, water, or arrows.

* Resource Die D6 - `resd6`
* Resource Die D8 - `resd8`
* Resource Die D10 - `resd10`
* Resource Die D12 - `resd12`

### Negative Dice
For when you have a negative bonus modifier.

* Negative D6 - `nt/nv`

### Numbered Dice
For when you need an actual number on the die. You can also add `-an` to any command to see the actual numbers rolled.

* Regular D6 - `d6`

### Notes
When you need to add a note or comment to your roll, use "". To prevent the numbers from shuffling around, we can add the flag `-ns`.
`>roll 2resd8 "Food/Water" -ns`
