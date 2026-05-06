@echo off
echo 🚀 Starting deployment of Quarto course website...

:: 1. Add all changes to git
git add .

:: 2. Commit with a generic update message
git commit -m "Automated update to course website"

:: 3. Push source files to GitHub
echo Pushing source files to GitHub...
git push

:: 4. Use Quarto to render and publish the site to gh-pages
echo Rendering and publishing HTML to GitHub Pages...
quarto publish gh-pages --no-prompt

echo ✅ Deployment complete! Your website should update in a few minutes.
pause
