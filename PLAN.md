# Plan: Soldat on Android

Written 2026-10-16 from desk research and a read of the open source code. **Nothing here has been built or tested yet.** Anything marked *(unverified)* is a belief, not a fact. Anything marked *(estimate)* is a rough guess for one person working part time.

## 1. What we are starting from (checked)

- The open source version is "1.8", at <https://github.com/soldat/soldat>. Code licence: MIT. Game art and data live in a separate repository, <https://github.com/opensoldat/base>, under Creative Commons Attribution 4.0.
- Size of the Pascal code in that repository (counted by us on 2026-10-16): about 36,000 lines in the client, 21,000 in the server and 47,000 shared. So roughly 83,000 lines for the client side to carry to a phone.
- The upstream repository's last code change was in July 2022. The project looks quiet. Nobody is obviously maintaining it for us. *(Whether a newer active fork exists is unverified.)*
- Language: Free Pascal. Libraries: SDL2 (window, input), OpenAL (sound), FreeType (text), PhysFS (reads the game data archive), GameNetworkingSockets (online play).
- The client draws with **desktop OpenGL**. Its shaders say `#version 120` (an old desktop shader language), and it loads OpenGL through a desktop loader (`dglOpenGL`). Phones use **OpenGL ES**, a smaller cousin. There is a commented-out "OPENGL ES3 TEST" in the window setup code, so the authors thought about it but did not finish.
- The client reads **mouse and keyboard** only. We found no touch handling in it.

## 2. The options

### Option A: Native Android app built with Free Pascal (recommended to try first)

Free Pascal can make code for Android on 64-bit phone processors (the "arm64" target). Its own wiki says this works from Free Pascal 3.2 onward, and prebuilt cross compilers are published (version 3.2.2, plus daily snapshots of the 3.3.1 development line). The upstream notes ask for Free Pascal 3.0.4, so the code may need small changes for a newer compiler *(unverified)*.

How it would fit together:

1. Android Native Development Kit supplies the C compiler and system files.
2. Build SDL2, OpenAL Soft, FreeType, PhysFS and GameNetworkingSockets as Android libraries for arm64.
3. Turn the game from a *program* into a *shared library* (`libmain.so`) that SDL2's own Java starter code (`SDLActivity`) loads. People who ship Free Pascal games on Android report this is the way: SDL2 cannot start without its Java layer.
4. Package everything with Gradle into an installable Android file, with the game data inside.

Good: keeps one code base, keeps desktop and phone close. Hard: the graphics and touch parts (below) are real rewrites.

### Option B: Pascal-to-C, or another language

We know of no mainstream Pascal-to-C route that would beat the direct Free Pascal Android target *(unverified: we did not search deeply)*. Rewriting the client in another language or engine would be a rewrite of about 80,000 lines. **Not recommended.**

### Option C: Play in the browser (WebAssembly)

Free Pascal has an early WebAssembly target *(unverified how ready it is)*. Browsers cannot send the raw UDP packets the game's network library uses, so online play would need a relay server. Bigger and riskier than Option A. Keep as a "maybe much later".

### Option D: Simple fallback, today

Link to <https://soldat.pl> and let people use the Windows game with a workaround (remote desktop, Windows emulation, or a game streaming service). No work, bad experience on a phone. This is what the popcorn launcher does now, and stays as the fallback.

## 3. The hard parts (the honest list)

| Part | Why it is hard | Size (estimate) |
|---|---|---|
| Toolchain | Free Pascal cross compiler + Android Native Development Kit + Gradle must all agree. Many small version traps. | 1 to 2 weeks |
| Helper libraries | Five libraries to cross build for arm64. GameNetworkingSockets needs OpenSSL and protobuf too. Its newest releases list Android support; the 1.4.0 version the game names is older, so we would likely move to a newer one and check the Pascal bindings still match. *(unverified)* | 1 to 3 weeks |
| Graphics | Rewrite shaders from desktop language to OpenGL ES language, swap the desktop loader, check every drawing call against what OpenGL ES allows. Visual bugs likely. | 2 to 4 weeks |
| Touch controls | The game is built for mouse aim plus many keys. A phone needs on-screen sticks and buttons for move, aim, shoot, jump, crouch, weapon change, reload, grenade, chat. Aiming on a touch screen is the biggest feel problem. | 3 to 6 weeks |
| Phone layout | Menus, text and the heads-up display are sized for a desktop window. Fingers need big targets. | 2 to 4 weeks |
| Networking | Mobile networks change address and drop packets. Need to confirm the 1.8 client can join the servers on soldat.pl at all: the live servers may run a different version *(unverified, important)*. | 1 to 3 weeks |
| Speed and battery | Unknown until tested on real phones. | 2 to 4 weeks |
| Packaging | Game data size, first-run download or bundled, Android storage rules. | 1 to 2 weeks |

Total, very roughly: **about 3 to 6 months of part time work for one person to get a playable test build** *(estimate, wide error bars)*. A polished public release is longer.

## 4. Things that could stop or change the plan

- The live servers may not accept the open source 1.8 client. If so, a phone player could only join servers running 1.8 *(unverified)*.
- Using the name "Soldat" and the soldat.pl brand for a public app needs a conversation with the authors. Not checked.
- Google Play has its own rules (64-bit, recent Android target version, content ratings for a violent game). Details not checked. Sideloading an installable file for friends avoids this at first.
- Upstream code is quiet since 2022, so we carry our own patches.

## 5. Order of work

Follows the milestones in [STATUS.md](STATUS.md):

1. Build the desktop game from source on Linux first. If that fails, nothing else matters.
2. Get Free Pascal to open an empty SDL2 window on a real phone.
3. Build the libraries, then get the menu on screen (graphics port).
4. Add touch controls to a single-player test map.
5. Join a real server.
6. Phone layout, sound, speed.
7. Friends test build. Then decide about a public release.

## 6. What we will not do

- Copy game binaries or game data into this repository from other places.
- Hide or remove the authors' names or licence texts.
- Promise dates. The sizes above are estimates.

## Sources used

- Soldat source and notes: <https://github.com/soldat/soldat> (README, CMake files, client Pascal files, checked 2026-10-16)
- Soldat game data and licence: <https://github.com/opensoldat/base>
- Free Pascal on Android: <https://wiki.freepascal.org/Android>, <https://www.freepascal.org/down/android/android-canada.var>
- SDL2 on Android: <https://wiki.libsdl.org/SDL2/Android>
- Free Pascal with SDL2 on Android (Java starter layer): <https://github.com/PascalGameDevelopment/SDL2-for-Pascal/issues/146>
- GameNetworkingSockets releases and Android notes: <https://github.com/ValveSoftware/GameNetworkingSockets/releases>
- Android Native Development Kit with CMake: <https://developer.android.com/ndk/guides/cmake>
