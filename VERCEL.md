# Vercel Deployment

This repository can be deployed to Vercel as a static website using `index.html`.

## Steps to connect to Vercel

1. Push your repository to GitHub.
2. Go to https://vercel.com and sign in with GitHub.
3. Import the project and select this repository.
4. For the project settings:
   - Framework preset: `Other`
   - Root directory: `/`
   - Build command: leave blank
   - Output directory: `/`
5. Deploy.

## Continuous deployment

Once the repository is connected, Vercel will automatically redeploy on every push to the linked branch.

## Notes

- This config deploys the static `index.html` frontend.
- The current project backend is a Flask/Celery pipeline and requires a separate server capable of running Python, Redis, and the bioinformatics tools.
- For full pipeline functionality, host the backend on a dedicated service and update the frontend to call that backend URL.
