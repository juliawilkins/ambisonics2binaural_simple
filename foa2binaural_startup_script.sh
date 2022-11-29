#!/bin/bash

# First make and activate the conda environment
conda create --name foa2binaural python=3.8
conda activate foa2binaural

# Install ffmpeg with onda
conda install -c conda-forge ffmpeg
pip install pybind11
pip install tqdm

# Download the precompiled IEM plugins
ggID='1g-QTK7CUjc2WyEUHBXQut_Ag9827MPLw'  
ggURL='https://drive.google.com/uc?export=download'  
filename="$(curl -sc /tmp/gcokie "${ggURL}&id=${ggID}" | grep -o '="uc-name.*</span>' | sed 's/.*">//;s/<.a> .*//')"  
getcode="$(awk '/_warning_/ {print $NF}' /tmp/gcokie)"  
curl -Lb /tmp/gcokie "${ggURL}&confirm=${getcode}&id=${ggID}" -o "${filename}"  
unzip "${filename}"  
cd 'VST3'
cp -r IEM/ ~/Library/Audio/Plug-Ins/VST3/
cd '../'
rm "${filename}"  
rm -r 'VST3/'
rm -r 'VST2/'

# Install Pedalboard from source 
# Make small change to code to allow for more than two channel input
git clone --recurse-submodules --shallow-submodules https://github.com/spotify/pedalboard.git
cd "pedalboard"
# Remove channel limit
git am << 'EOF2'
diff --git a/pedalboard/BufferUtils.h b/pedalboard/BufferUtils.h
index d5f2e40..5958cae 100644
--- a/pedalboard/BufferUtils.h
+++ b/pedalboard/BufferUtils.h
@@ -81,8 +81,6 @@ copyPyArrayIntoJuceBuffer(const py::array_t<T, py::array::c_style> inputArray) {
 
   if (numChannels == 0) {
     throw std::runtime_error("No channels passed!");
-  } else if (numChannels > 2) {
-    throw std::runtime_error("More than two channels received!");
   }
 
   juce::AudioBuffer<T> ioBuffer(numChannels, numSamples);
EOF2
pip install .


