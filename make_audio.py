"""Make Sparkle Blocks' sounds with ElevenLabs, once.

    python3 make_audio.py        sound effects, Jessica's cheers and the music -> sounds/

The API key is read from ~/.elevenlabs_key and never printed. Files already made are skipped.
"""
import json, ssl, sys, time, urllib.request
from pathlib import Path
import certifi

HERE = Path(__file__).resolve().parent
OUT = HERE / 'sounds'
KEY = (Path.home() / '.elevenlabs_key').read_text().strip()
CTX = ssl.create_default_context(cafile=certifi.where())
JESSICA = 'cgSgspJ2msm6clMCkdW9'      # the kind American voice Margot chose for Tick-Tock

SFX = {
    'pick': ('a tiny soft bubbly pop, like picking up a jelly sweet', 0.5),
    'place': ('a soft satisfying wooden block click, gentle and toy-like', 0.5),
    'clear1': ('a bright magical sparkle whoosh with tinkling chimes', 1.0),
    'clear2': ('a bigger magical sparkle whoosh with rising glittering chimes', 1.3),
    'clear3': ('a huge magical burst of sparkles and rising harp glissando, very happy', 1.8),
    'fanfare': ('a short happy magical fanfare with bells and sparkles, celebratory', 2.0),
    'gameover': ('a gentle soft music box melody that winds down, calm and friendly, not sad', 2.2),
}
LINES = {
    'v-combo': 'Combo!', 'v-supercombo': 'Super combo! Wow!', 'v-double': 'Double!', 'v-amazing': 'Amazing!',
    'v-allclear': 'All clear! Brilliant!', 'v-newbest': 'A new best score! Well done!',
    'v-greatbest': 'What a game! A brand new best score!', 'v-greatgame': "Great game! Let's play again!",
    'v-hello-margot': "Hello Margot! Let's make some sparkles!", 'v-hello': "Hello! Let's make some sparkles!",
    'v-hello-manon': "Hello Manon! Let's make some sparkles!",
}
# Nevermore: Manon's gothic theme. Deadpan, but always kind.
GSFX = {
    'g-pick': ('a tiny soft dark wooden tap, subtle and short', 0.5),
    'g-place': ('a muted heavy stone block set down on stone, short and satisfying', 0.5),
    'g-clear1': ('a single raven caw with a soft whoosh of black wings', 1.2),
    'g-clear2': ('a rumble of distant thunder with bat wings flapping away', 1.6),
    'g-clear3': ('a dramatic gothic pipe organ chord with a crack of thunder', 2.0),
    'g-fanfare': ('a short dramatic gothic pipe organ flourish, triumphant and spooky', 2.2),
    'g-gameover': ('a slow music box playing a sweet, slightly spooky lullaby that winds down', 2.4),
}
GLINES = {
    'g-combo': 'Combo. Delightfully destructive.', 'g-supercombo': 'A super combo. I am almost smiling.',
    'g-double': 'Two at once. Efficient.', 'g-amazing': 'Magnificent. Truly.', 'g-allclear': 'Everything is gone. Perfect.',
    'g-newbest': 'A new best score. Darkly magnificent.', 'g-greatbest': 'A new record. I knew you had it in you.',
    'g-greatgame': 'A worthy game. Again?', 'g-hello-manon': 'Hello, Manon. Shall we destroy some blocks?',
    'g-hello-margot': 'Hello, Margot. Shall we destroy some blocks?', 'g-hello': 'Hello. Shall we destroy some blocks?',
}
GMUSIC = ("A seamless looping instrumental for a gothic children's puzzle game, darkly elegant and quirky: harpsichord, "
          "pizzicato strings and soft cello, a little spooky but playful and calm, medium-slow tempo, no vocals, no drums")
GOTH_DESC = ("A calm, deadpan young woman with a soft, clear British accent, dry and darkly witty like a gothic heroine, "
             "speaking slowly and quietly, secretly warm and approving, never mean")
MUSIC = ("A seamless looping instrumental for a calm, happy children's puzzle game: soft marimba, celesta and gentle "
         "synth pads, light and dreamy, medium-slow tempo, sparkly, relaxing, no vocals, no drums")


def post(path, body):
    req = urllib.request.Request('https://api.elevenlabs.io/v1' + path, data=json.dumps(body).encode(),
                                 headers={'xi-api-key': KEY, 'Content-Type': 'application/json'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=240, context=CTX) as r:
                return r.read()
        except Exception as e:
            print('  retry', path, e); time.sleep(3)
    raise RuntimeError('failed ' + path)


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for name, (prompt, secs) in SFX.items():
        f = OUT / f'{name}.mp3'
        if f.exists(): continue
        f.write_bytes(post('/sound-generation', {'text': prompt, 'duration_seconds': secs, 'prompt_influence': 0.5})); print('sfx', name)
    for name, text in LINES.items():
        f = OUT / f'{name}.mp3'
        if f.exists(): continue
        f.write_bytes(post(f'/text-to-speech/{JESSICA}?output_format=mp3_44100_128', {'text': text, 'model_id': 'eleven_multilingual_v2',
                           'voice_settings': {'stability': 0.4, 'similarity_boost': 0.8, 'style': 0.45, 'use_speaker_boost': True}})); print('line', name)
    f = OUT / 'music.mp3'
    if not f.exists():
        f.write_bytes(post('/music', {'prompt': MUSIC, 'music_length_ms': 60000})); print('music')
    # the gothic voice: designed once, kept in voice_goth.json
    vf = HERE / 'voice_goth.json'
    if not vf.exists():
        import base64
        pv = json.loads(post('/text-to-voice/create-previews', {'voice_description': GOTH_DESC,
             'text': 'Combo. Delightfully destructive. A new best score, darkly magnificent. I knew you had it in you. Shall we destroy some more blocks?'}))
        pdir = HERE / 'voice_previews'; pdir.mkdir(exist_ok=True)
        for i, p in enumerate(pv['previews']): (pdir / f'goth-{i + 1}.mp3').write_bytes(base64.b64decode(p['audio_base_64']))
        v = json.loads(post('/text-to-voice/create-voice-from-preview', {'voice_name': 'Block Blitz Nevermore', 'voice_description': GOTH_DESC,
            'generated_voice_id': pv['previews'][0]['generated_voice_id']}))
        vf.write_text(json.dumps({'goth': v['voice_id'], 'previews': [p['generated_voice_id'] for p in pv['previews']]})); print('designed the gothic voice')
    GOTH = json.loads(vf.read_text())['goth']
    for name, (prompt, secs) in GSFX.items():
        f = OUT / f'{name}.mp3'
        if f.exists(): continue
        f.write_bytes(post('/sound-generation', {'text': prompt, 'duration_seconds': secs, 'prompt_influence': 0.5})); print('sfx', name)
    for name, text in GLINES.items():
        f = OUT / f'{name}.mp3'
        if f.exists(): continue
        f.write_bytes(post(f'/text-to-speech/{GOTH}?output_format=mp3_44100_128', {'text': text, 'model_id': 'eleven_multilingual_v2',
                           'voice_settings': {'stability': 0.6, 'similarity_boost': 0.8, 'style': 0.3, 'use_speaker_boost': True}})); print('line', name)
    f = OUT / 'g-music.mp3'
    if not f.exists():
        f.write_bytes(post('/music', {'prompt': GMUSIC, 'music_length_ms': 60000})); print('g-music')
    (OUT / 'manifest.json').write_text(json.dumps(sorted(p.stem for p in OUT.glob('*.mp3') if p.stat().st_size > 1000)))
    print('done:', len(list(OUT.glob('*.mp3'))), 'files')
