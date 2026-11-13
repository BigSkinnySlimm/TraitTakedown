using System;
using UnityEngine;

namespace TraitTakedown.Audio
{
    /// <summary>
    /// Native 48kHz Real-Time Floating-Point Symphonic Pad & Foley DSP Synthesizer
    /// Runs on Unity's native audio thread via OnAudioFilterRead with Concert Hall Reverb.
    /// </summary>
    [RequireComponent(typeof(AudioSource))]
    public class NativeSymphonicAudioDSP : MonoBehaviour
    {
        public static NativeSymphonicAudioDSP Instance { get; private set; }
        public bool IsMuted { get; private set; }

        private double _sampleRate = 48000.0;
        private double _dspTime;
        private int _chordIndex;
        private double _chordTimer;

        // D-minor 9th Symphonic Progression (Dm9 -> Bbmaj9 -> Gm9 -> A7sus4)
        private readonly double[][] _chords = new double[][]
        {
            new double[] { 73.42, 146.83, 220.00, 261.63, 329.63 },
            new double[] { 58.27, 116.54, 220.00, 293.66, 392.00 },
            new double[] { 49.00, 146.83, 196.00, 220.00, 293.66 },
            new double[] { 55.00, 164.81, 220.00, 277.18, 329.63 }
        };

        private readonly double[] _phasesA = new double[5];
        private readonly double[] _phasesB = new double[5];

        // Foley & Tactical SFX Envelope States
        private double _sfxFreq;
        private double _sfxPhase;
        private double _sfxAmp;
        private double _sfxDecay = 0.9992;

        // Stereo Delay Buffer for Concert Hall Reverb
        private float[] _reverbBufferL;
        private float[] _reverbBufferR;
        private int _reverbWriteIdx;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;
            DontDestroyOnLoad(gameObject);

            _sampleRate = AudioSettings.outputSampleRate > 0 ? AudioSettings.outputSampleRate : 48000.0;
            int delaySamples = Mathf.Max(4096, (int)(_sampleRate * 0.32));
            _reverbBufferL = new float[delaySamples];
            _reverbBufferR = new float[delaySamples];

            var src = GetComponent<AudioSource>();
            src.playOnAwake = true;
            src.loop = true;
            src.spatialBlend = 0f;
            src.Play();
        }

        public bool ToggleMute()
        {
            IsMuted = !IsMuted;
            return IsMuted;
        }

        public void PlayCardFlipFoley()
        {
            _sfxFreq = 165.0;
            _sfxAmp = 0.24;
            _sfxDecay = 0.9985;
        }

        public void PlayRadarScanFoley()
        {
            _sfxFreq = 523.25;
            _sfxAmp = 0.22;
            _sfxDecay = 0.9994;
        }

        public void PlayAbilityUltimateBoom()
        {
            _sfxFreq = 110.0;
            _sfxAmp = 0.35;
            _sfxDecay = 0.99965;
        }

        private void OnAudioFilterRead(float[] data, int channels)
        {
            if (IsMuted || _reverbBufferL == null)
            {
                Array.Clear(data, 0, data.Length);
                return;
            }

            double dt = 1.0 / _sampleRate;
            int bufLen = _reverbBufferL.Length;

            for (int i = 0; i < data.Length; i += channels)
            {
                _dspTime += dt;
                _chordTimer += dt;
                if (_chordTimer >= 5.2)
                {
                    _chordTimer = 0.0;
                    _chordIndex = (_chordIndex + 1) % _chords.Length;
                }

                double[] chord = _chords[_chordIndex];
                double env = Math.Sin((_chordTimer / 5.2) * Math.PI);
                double padSumL = 0.0;
                double padSumR = 0.0;

                for (int v = 0; v < 5; v++)
                {
                    double freq = chord[v];
                    _phasesA[v] += (freq * dt) * 2.0 * Math.PI;
                    _phasesB[v] += (freq * 1.0035 * dt) * 2.0 * Math.PI;

                    double warmWaveA = Math.Sin(_phasesA[v]) + 0.35 * Math.Sin(_phasesA[v] * 2.0);
                    double warmWaveB = Math.Sin(_phasesB[v]) + 0.35 * Math.Cos(_phasesB[v] * 2.0);

                    double voiceGain = (v == 0) ? 0.045 : 0.022;
                    padSumL += warmWaveA * voiceGain * env;
                    padSumR += warmWaveB * voiceGain * env;
                }

                // Foley / SFX Layer
                double sfxSample = 0.0;
                if (_sfxAmp > 0.0001)
                {
                    _sfxPhase += (_sfxFreq * dt) * 2.0 * Math.PI;
                    sfxSample = Math.Sin(_sfxPhase) * _sfxAmp;
                    _sfxAmp *= _sfxDecay;
                }

                // Concert Hall Feedback Reverb
                float wetL = _reverbBufferL[_reverbWriteIdx];
                float wetR = _reverbBufferR[_reverbWriteIdx];

                float outL = (float)(padSumL + sfxSample) + wetL * 0.38f;
                float outR = (float)(padSumR + sfxSample) + wetR * 0.38f;

                _reverbBufferL[_reverbWriteIdx] = outR * 0.46f;
                _reverbBufferR[_reverbWriteIdx] = outL * 0.46f;
                _reverbWriteIdx = (_reverbWriteIdx + 1) % bufLen;

                data[i] = Mathf.Clamp(outL, -0.95f, 0.95f);
                if (channels > 1)
                {
                    data[i + 1] = Mathf.Clamp(outR, -0.95f, 0.95f);
                }
            }
        }
    }
}
