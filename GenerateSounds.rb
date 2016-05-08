#!/usr/bin/ruby
fileContent = `cat SoundSymbolCombos.txt`
combos = fileContent.split("\n")
tones = ["", "ˊ", "ˇ", "ˋ", "˙"]
for tone in tones
	for combo in combos
		word = combo+tone
		`say -o #{word}.wav --data-format=UI8@8000 #{word}`
	end
end
