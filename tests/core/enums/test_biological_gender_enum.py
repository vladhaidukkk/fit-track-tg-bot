from bot.core.enums.biological_gender import BiologicalGender


class TestBiologicalGenderEnum:
    def test_has_only_two_members(self) -> None:
        assert len(BiologicalGender) == 2

    def test_has_male_member(self) -> None:
        assert "MALE" in BiologicalGender.__members__

    def test_has_female_member(self) -> None:
        assert "FEMALE" in BiologicalGender.__members__
