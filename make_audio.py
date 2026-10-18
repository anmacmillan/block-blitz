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
    'v-hello-manon': "Hello Manon! Let's make some sparkles!", 'v-hello-dad': "Hello Dad! Let's make some sparkles!",
    'v-trophy': 'A new trophy! Well done!', 'v-unlock': 'Ooh! New blocks to play with!',
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
BOSS_SFX = {
    'boss-roar': ('a cartoon dragon giving a big grumbly roar, funny and dramatic, not scary', 2.0),
    'boss-attack': ('a whoosh of dark cartoon magic flying through the air and landing with a heavy thud', 1.4),
}
GLINES = {
    'g-combo': 'Combo. Delightfully destructive.', 'g-supercombo': 'A super combo. I am almost smiling.',
    'g-double': 'Two at once. Efficient.', 'g-amazing': 'Magnificent. Truly.', 'g-allclear': 'Everything is gone. Perfect.',
    'g-newbest': 'A new best score. Darkly magnificent.', 'g-greatbest': 'A new record. I knew you had it in you.',
    'g-greatgame': 'A worthy game. Again?', 'g-hello-manon': 'Hello, Manon. Shall we destroy some blocks?',
    'g-hello-margot': 'Hello, Margot. Shall we destroy some blocks?', 'g-hello': 'Hello. Shall we destroy some blocks?', 'g-hello-dad': 'Hello, Dad. Shall we destroy some blocks?',
    'g-trophy': 'A trophy. How splendid.', 'g-unlock': 'New blocks. Delightfully dark.',
}
GMUSIC = ("A seamless looping instrumental for a gothic children's puzzle game, darkly elegant and quirky: harpsichord, "
          "pizzicato strings and soft cello, a little spooky but playful and calm, medium-slow tempo, no vocals, no drums")
GOTH_DESC = ("A calm, deadpan young woman with a soft, clear British accent, dry and darkly witty like a gothic heroine, "
             "speaking slowly and quietly, secretly warm and approving, never mean")
# the warm encouraging narrator: an original voice, designed from a description (not a copy of anyone)
WARM_DESC = ("A warm, low, slightly husky American woman's voice in her thirties, smooth, relaxed and intimate, "
             "with a gentle smile in it; kind, calm and encouraging, speaking unhurriedly")
WLINES = {
    'w-end-0': "You're getting better every single game.", 'w-end-1': "Mmm, that was a lovely game. Want another?",
    'w-end-2': "I love how carefully you're thinking.", 'w-end-3': "Every game makes your brain a little stronger.",
    'w-end-4': "You've got a real eye for this.", 'w-end-5': "Nicely done. I'm proud of you.",
    'w-end-6': "Take a breath. You've got this.", 'w-end-7': "That was some clever playing. Well done, you.",
    'w-nice-0': 'Ooh, beautiful.', 'w-nice-1': 'Look at you go!', 'w-nice-2': "Oh, that's gorgeous.",
    'w-nice-3': 'Clever.', 'w-nice-4': 'Lovely move.', 'w-nice-5': 'Mmm, very nice.',
    'w-rank-s-1': "You've risen to the Archangels.", 'w-rank-s-2': 'Welcome to the Principalities.', 'w-rank-s-3': 'Now you are one of the Powers.',
    'w-rank-s-4': 'The Virtues. You are shining.', 'w-rank-s-5': 'The Dominions. Higher and higher.', 'w-rank-s-6': 'The Thrones. Look how far you have come.',
    'w-rank-s-7': 'The Cherubim. Almost at the top.', 'w-rank-s-8': 'The Seraphim. The very highest of all. You did it.',
    'w-rank-g-1': 'A Wraith now. Rather elegant.', 'w-rank-g-2': 'A Raven. Clever and dark.', 'w-rank-g-3': 'A Banshee. Wonderfully eerie.',
    'w-rank-g-4': 'A Gargoyle. Strong as stone.', 'w-rank-g-5': 'A Vampire. Ooh, impressive.', 'w-rank-g-6': 'A Necromancer. Very powerful.',
    'w-rank-g-7': 'A Lich. Nearly at the top.', 'w-rank-g-8': 'Queen of the Night. You rule the darkness now. Magnificent.',
}
# the arcade announcer: an original voice, designed from a description
ANN_DESC = ("A booming, energetic arcade fighting-game announcer: a deep, gravelly man's voice, dramatic and hyped, "
            "shouting short phrases with huge excitement, echoing like a stadium")
SHOUTS = {
    'blast': ['Blast!', 'Smash!', 'Kapow!', 'Boom!'], 'double': ['Double blast!', 'Double trouble!', 'Two at once!'],
    'triple': ['Triple blast!', 'Hat trick!', 'Triple threat!'], 'mega': ['Mega blast!', 'Monster blast!'],
    'combo': ['Combo!', 'Keep it going!', 'Again!'], 'supercombo': ['Super combo!', 'On fire!', 'Red hot!'],
    'ultra': ['Ultra combo!', 'Unstoppable!', 'Spectacular!'], 'perfect': ['Perfect!', 'Flawless!'],
}
ALINES = {f'a-{k}-{i}': t for k, v in SHOUTS.items() for i, t in enumerate(v)}
ALINES.update({
    'a-blast': 'Blast!', 'a-double': 'Double blast!', 'a-triple': 'Triple blast!', 'a-mega': 'Mega blast!',
    'a-combo': 'Combo!', 'a-supercombo': 'Super combo!', 'a-ultra': 'Ultra combo!', 'a-perfect': 'Perfect!',
    'a-hundred': 'One hundred!', 'a-thousand': 'One thousand! Incredible!', 'a-unstoppable': 'Unstoppable!',
    'a-legend': 'Ten thousand! Legendary!', 'a-record': 'New record!', 'a-trophy': 'Trophy unlocked!',
    'a-rankup': 'Rank up!', 'a-ascend': 'Ascension complete!',
    'a-boss': 'Here comes the boss!', 'a-bossdown': 'Boss defeated!',
})
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
    for name, (prompt, secs) in BOSS_SFX.items():
        f = OUT / f'{name}.mp3'
        if f.exists(): continue
        f.write_bytes(post('/sound-generation', {'text': prompt, 'duration_seconds': secs, 'prompt_influence': 0.5})); print('sfx', name)
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
    wf = HERE / 'voice_warm.json'
    if not wf.exists():
        import base64
        pv = json.loads(post('/text-to-voice/create-previews', {'voice_description': WARM_DESC,
             'text': "Mmm, that was a lovely game. You're getting better every single game, and I love how carefully you're thinking. Take a breath. You've got this."}))
        pdir = HERE / 'voice_previews'; pdir.mkdir(exist_ok=True)
        for i, p in enumerate(pv['previews']): (pdir / f'warm-{i + 1}.mp3').write_bytes(base64.b64decode(p['audio_base_64']))
        v = json.loads(post('/text-to-voice/create-voice-from-preview', {'voice_name': 'Block Blitz Warm', 'voice_description': WARM_DESC,
            'generated_voice_id': pv['previews'][0]['generated_voice_id']}))
        wf.write_text(json.dumps({'warm': v['voice_id'], 'previews': [p['generated_voice_id'] for p in pv['previews']]})); print('designed the warm voice')
    WARM = json.loads(wf.read_text())['warm']
    for name, text in WLINES.items():
        f = OUT / f'{name}.mp3'
        if f.exists(): continue
        f.write_bytes(post(f'/text-to-speech/{WARM}?output_format=mp3_44100_128', {'text': text, 'model_id': 'eleven_multilingual_v2',
                           'voice_settings': {'stability': 0.45, 'similarity_boost': 0.8, 'style': 0.4, 'use_speaker_boost': True}})); print('line', name)
    af = HERE / 'voice_announcer.json'
    if not af.exists():
        import base64
        pv = json.loads(post('/text-to-voice/create-previews', {'voice_description': ANN_DESC,
             'text': 'Round one! Fight! Double blast! Super combo! Ultra combo! Perfect! New record! Unstoppable! Ten thousand! Legendary!'}))
        pdir = HERE / 'voice_previews'; pdir.mkdir(exist_ok=True)
        for i, p in enumerate(pv['previews']): (pdir / f'announcer-{i + 1}.mp3').write_bytes(base64.b64decode(p['audio_base_64']))
        v = json.loads(post('/text-to-voice/create-voice-from-preview', {'voice_name': 'Block Blitz Announcer', 'voice_description': ANN_DESC,
            'generated_voice_id': pv['previews'][0]['generated_voice_id']}))
        af.write_text(json.dumps({'announcer': v['voice_id']})); print('designed the announcer')
    ANN = json.loads(af.read_text())['announcer']
    for name, text in ALINES.items():
        f = OUT / f'{name}.mp3'
        if f.exists(): continue
        f.write_bytes(post(f'/text-to-speech/{ANN}?output_format=mp3_44100_128', {'text': text, 'model_id': 'eleven_multilingual_v2',
                           'voice_settings': {'stability': 0.3, 'similarity_boost': 0.85, 'style': 0.8, 'use_speaker_boost': True}})); print('line', name)
    f = OUT / 'cello.mp3'
    if not f.exists():
        f.write_bytes(post('/music', {'prompt': ("A calm, cerebral solo cello piece in the baroque style of a cello suite prelude: flowing arpeggios, "
            "warm and resonant, contemplative and gentle, steady tempo, seamless loop, no other instruments, no vocals"), 'music_length_ms': 90000})); print('cello')
    (OUT / 'manifest.json').write_text(json.dumps(sorted(p.stem for p in OUT.glob('*.mp3') if p.stat().st_size > 1000)))
    print('done:', len(list(OUT.glob('*.mp3'))), 'files')
