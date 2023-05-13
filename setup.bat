@echo off
python --version && python -m venv env && CALL env\Scripts\activate && python -m pip install --upgrade pip && python -m pip install -r requirements.txt && (
  echo FERTIG
) || (
  echo FEHLGESCHLAGEN
)
echo Enter zum beenden.
pause >nul