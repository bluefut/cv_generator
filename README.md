# Sample ATS-Friendly PDF CV Generator

Install requirements:
```sh
pip install reportlab svglib
```

## Usage
1. Place the SVG icons for email, phone, location, LinkedIn in the same directory as `cv_generator.py`. Use these filenames:
   - `mail.svg`
   - `tel.svg`
   - `location.svg`
   - `linkedin.svg`
2. Edit `cv_generator.py` to customize the fields (skills, jobs, education, contact, etc).
3. Run the script:
```sh
python cv_generator.py
```
4. Output will be saved as `Sample_CV.pdf` in the same folder.
