# FOA to Binaural Audio
A simple Python script to convert FOA audio to binaural. This uses Spotify's [pedalboard](https://github.com/spotify/pedalboard) package, which allows for loading of VSTs. This script is designed to use [IEM's Binaural Decoder plug-in](https://plugins.iem.at/docs/plugindescriptions/#binauraldecoder).


# Usage 
## Setup
1. Clone this repository.
2. The environment and package download setup is a bit complicated. Run `bash foa2binaural_startup_script.sh` to:
    - Create a conda environment to install your packages in
    - Download pedalboard and make a small change to their code to allow for more than 2-channel audio processing
    - Downloading the IEM plug-ins and move this to the appropriate spot on your local. Note you may need to edit the startup script to ensure that these paths are correct for your environment. You eventually need to have the BinauralDecoder.vst here: `/Library/Audio/Plug-Ins/VST3/IEM/BinauralDecoder.vst3/`

## Converting your audio
To convert FOA audio to binaural, here's an example command:
```
python foa2binaural_script.py --input_filepath fold4_room2_mix002.wav --output_filepath test.wav
```
Ta-da!

## Credits
Many thanks to @auroracramer for the meat (or the beans, for us herbivores) of this code and the idea to use pedalboard with the IEM plugins!
