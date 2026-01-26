# PC1: Download Command (Quick Reference)

## Single Command to Download Everything

**Run this on PC1 (with internet):**

```powershell
mkdir C:\pip_packages; cd C:\pip_packages; pip download -r "C:\path\to\requirements.txt" -d .
```

Replace `"C:\path\to\requirements.txt"` with actual path to requirements.txt

## Alternative: Step-by-Step

```powershell
# Step 1: Create folder
mkdir C:\pip_packages

# Step 2: Go to folder
cd C:\pip_packages

# Step 3: Download all packages (adjust path to requirements.txt)
pip download -r "C:\Projects\RBAC_Project\requirements.txt" -d .
```

## Verify Download

Check folder has 13 .whl files:
```powershell
dir C:\pip_packages
```

You should see files like:
- Django-4.2.7-py3-none-any.whl
- pandas-2.1.3-cp310-cp310-win_amd64.whl
- numpy-1.26.4-cp310-cp310-win_amd64.whl
- etc.

## Copy to USB

```powershell
Copy-Item -Path "C:\pip_packages" -Destination "E:\pip_packages" -Recurse
```

(Replace E:\ with your USB drive letter)

---

## What This Creates

- **Total files**: 13 wheel packages (~200-300MB)
- **No internet needed on PC2** after download
- **All dependencies included** (no hidden requirements)
- **Transferable via USB** to any PC with Python 3.8+

---

**That's all you need from PC1!** 🎉
