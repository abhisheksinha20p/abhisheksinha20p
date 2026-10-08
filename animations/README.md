# Profile Animation Studio

This folder contains the Framer Motion source for the animated visual system used by the GitHub profile.

## Included animations

- Contribution Shooter
- Production Pipeline
- Technology Orbit
- Engineering Evolution timeline
- Animated hero / gradient identity

## Run locally

```bash
cd animations
npm install
npm run dev
```

Then open the Vite development URL.

## Build

```bash
npm run build
```

The generated site will be in:

```text
animations/dist/
```

## GitHub README limitation

GitHub does not execute React or Framer Motion inside `README.md`.

For that reason, the README references pre-rendered assets such as:

```text
../assets/space-shooter.gif
```

You can render the React animations into GIF/WebM/MP4 assets using your preferred capture tool and place the resulting files in `assets/`.

The React implementation remains in this repository so the animations can be maintained and regenerated.
