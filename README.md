<h1>Syllable Detection</h1>
A single bird recording can be hours in length but only contain a couple minutes of song.

The file sizes of these recordings can be on the GB scales. Feeding such dat

Here I made a clever syllable detection algorithm using:

<ol>
    <li>Zero phase filtering.</li>
    <li>Moving average filters.</li>
    <li>Average amplitude values of syllables.</li>
    <li>Average Fourier / power spectrum of syllables </li>
</ol>

<h2>Syllable Characteristics</h2>
Here are the amplitudes and Fourier spectrums of the syllables of interest (labeled as: g,h,i,j).

<h2>Filtering</h2>
To denoise the original signal without introducing phase distortion, I implemented forwards-backwards filtering using a high pass filter. My choice of filter was an 8th order Chebyshev II filter. The cutoff frequency was chosen to be 320 Hz, with a minimum attenuation of -30 dB.<br><br>

The reasoning behind this choice is because the Chebyshev filter has a steeper transition band, and perfectly preserves the pass band while greatly attenuating lower frequency noise.
<br><br>
<img src = Figures/Mag_resp.png> 

<h2>Moving Average</h2>

<h2>Cutting</h2>
