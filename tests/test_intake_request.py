import sys, tempfile, shutil, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
import intake_request

class IntakeTests(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(intake_request.slugify("Pets & Trading.txt"), "pets-trading")

    def test_next_id_and_preserve_raw(self):
        with tempfile.TemporaryDirectory() as td:
            troot = Path(td)
            (troot/"00_INPUT/UPDATES/INBOX").mkdir(parents=True)
            (troot/"00_INPUT/UPDATES/PROCESSING").mkdir(parents=True)
            (troot/"00_INPUT/UPDATES/PROCESSED").mkdir(parents=True)
            (troot/"04_CHANGESETS").mkdir()
            shutil.copytree(ROOT/"templates", troot/"templates")
            (troot/"04_CHANGESETS/2026-01-01_U003_old").mkdir()

            intake_request.ROOT = troot
            intake_request.INBOX = troot/"00_INPUT/UPDATES/INBOX"
            intake_request.PROCESSING = troot/"00_INPUT/UPDATES/PROCESSING"
            intake_request.CHANGESETS = troot/"04_CHANGESETS"
            intake_request.TEMPLATE = troot/"templates/CHANGESET_TEMPLATE"

            self.assertEqual(intake_request.next_update_id(), "U004")
            src = intake_request.INBOX/"pets.txt"
            payload = b"Add pets.\r\nKeep bonuses moderate.\r\n"
            src.write_bytes(payload)
            cs = intake_request.create_changeset(src, "U004")
            self.assertEqual((cs/"USER_REQUEST.txt").read_bytes(), payload)
            self.assertTrue((intake_request.PROCESSING/"U004_pets.txt").exists())

if __name__ == "__main__":
    unittest.main()
