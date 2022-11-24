import pedalboard 
import os
import glob
from tqdm import tqdm
import argparse

def load_vst(binaural_decoder_vst_path):
    """Load the pedalboard VST.

    Args:
        binaural_decoder_vst_path (str): Path to VST. 
            Note this should be in: "/Library/Audio/Plug-Ins/VST3/IEM/BinauralDecoder.vst3/" 
            typically. 

    Returns:
        pedalboard vst: Loaded pedalboard VST plugin.
    """
    vst =  pedalboard.load_plugin(binaural_decoder_vst_path)
    return vst 

def set_vst_params(binaural_decoder_vst):
    """Sets parameters of the binaural decoder VST>

    Args:
        binaural_decoder_vst (pedalboard vst): Loaded pedalboard VST.

    Returns:
       pedalboard vst: Loaded pedalboard VST with updated parameters.
    """
    binaural_decoder_vst.bypass = False
    binaural_decoder_vst.input_ambisonic_order = "1st"
    binaural_decoder_vst.input_normalization = "N3D"
    return vst

def postprocess(audio):
    """ Grab the first two channels since the last two will just be silence
    after processing to binaural.

    Args:
        audio (pedalboard AudioFile): Ambisonics -> binaural audio,
            but still with 4 channels (last two silent).

    Returns:
       pedalboard AudioFile: 2-channel audio output.
    """
    
    return audio[:2]

def process(inp_path, out_path, binaural_decoder_vst):
    """Load the input audio and call the pedalboard VST
    to decode from ambisonics to binaural. Note this returns a 
    4-channel AudioFile, but with last 2 channels silent.

    Args:
        inp_path (str): Path to input ambisonics file.
        out_path (str: Path to output binaural file.
        binaural_decoder_vst (pedalboard vst): Loaded binaural VST.
    """
    # Convert to absolute paths to avoid pedalboard warnings
    inp_path = os.path.realpath(inp_path)
    out_path = os.path.realpath(out_path)
    with pedalboard.io.AudioFile(inp_path, 'r') as f:
        # NOTE: pedalboard loads audio in array of shape
        # (n_chan, n_samples), opposite of soundfile behavior
        inp_audio = f.read(f.frames)
        sr = f.samplerate
    out_audio = binaural_decoder_vst(inp_audio, sr)

    # Apply postprocessing
    out_audio = out_audio[:2] # This grabs the first two channels, last two are silence
    out_n_chan = out_audio.shape[0]
    
    with pedalboard.io.AudioFile(out_path, 'w', sr, out_n_chan) as f:
        f.write(out_audio)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_filepath", required=True, help="Path to your input ambisonics file.")
    parser.add_argument("--output_filepath", required=True, help="Path to your output binaural file.")
    args = parser.parse_args()

    # Hard-coding this path as it should be here for anyone
    vst = load_vst("/Library/Audio/Plug-Ins/VST3/IEM/BinauralDecoder.vst3/")
    vst = set_vst_params(vst)

    # This is setup to process a single file
    process(inp_path=args.input_filepath,
            out_path=args.output_filepath,
            binaural_decoder_vst=vst)

    # If you wanted to apply to every file in a nested dir:

    # binaural_path = 'foa_dev_binaural/'
    # all_dev_fpaths = glob.glob('foa_dev/*/*.wav')
    # for f in tqdm(all_dev_fpaths):
    #     new_fpath = binaural_path + '/'.join(f.split('/')[1:])
    #     process(inp_path=f,
    #             out_path=new_fpath,
    #             binaural_decoder_vst=vst)

        

