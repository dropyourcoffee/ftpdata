from ftpdata import preset
from ftpdata.exceptions import PresetValidationError
import pytest

class TestPreset:

    def test_1_load_preset(self):
        cfg = preset.Config('preset_sample')
        print(cfg.sync_db)
        assert cfg.sync_db.host == "localhost"

    def test_2_fail_when_presetfile_not_exists(self):
        cfg = preset.Config('non_existing_preset')
        print(cfg.sync_db)
        assert cfg.sync_db.host == "localhost"

    def test_3_validate_preset_has_sync_db(self):
        with pytest.raises(PresetValidationError):
            cfg = preset.Config('preset_sample_wrong')