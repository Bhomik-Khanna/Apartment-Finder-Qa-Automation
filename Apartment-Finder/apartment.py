

class Apartment:
    def __init__(self, name, address, rent, bedrooms, notes="", commute_minutes=None):
        self.name = name
        self.address = address
        self.rent = rent
        self.bedrooms = bedrooms
        self.notes = notes
        # commute_minutes starts as None because we don't know it yet —
        # distance_api.py will fill this in later, automatically.
        self.commute_minutes = commute_minutes

    def score(self, max_rent=30000, max_commute=60, rent_weight=0.6, commute_weight=0.4):
        """
        Returns a score from 0 to 100. Higher = better.

        The idea: cheaper rent and shorter commute both push the score up.
        We normalize each one to a 0-1 scale, then combine them using
        weights you choose (default: rent matters slightly more than commute).

        max_rent / max_commute are the "worst case" values used to scale
        the score — tune these to your own budget and patience for commuting.
        Defaults assume INR rent (e.g. ₹30,000/month as a rough upper bound;
        adjust to whatever's realistic for your city).
        """
        if self.commute_minutes is None:
            # Can't score fairly without commute data yet.
            return 0

        # Lower rent and lower commute should give a HIGHER score,
        # so we subtract the normalized value from 1.
        rent_score = 1 - (self.rent / max_rent)
        commute_score = 1 - (self.commute_minutes / max_commute)

        # Clamp scores to [0, 1] in case an apartment is way above the max
        # (e.g. rent higher than max_rent would otherwise go negative).
        rent_score = max(0, min(1, rent_score))
        commute_score = max(0, min(1, commute_score))

        combined = (rent_score * rent_weight) + (commute_score * commute_weight)
        return round(combined * 100, 1)

    def to_dict(self):
        """Convert this apartment into a plain dictionary, for saving to JSON."""
        return {
            "name": self.name,
            "address": self.address,
            "rent": self.rent,
            "bedrooms": self.bedrooms,
            "notes": self.notes,
            "commute_minutes": self.commute_minutes,
        }

    @classmethod
    def from_dict(cls, data):
        """Build an Apartment back from a dictionary (the reverse of to_dict)."""
        return cls(
            name=data["name"],
            address=data["address"],
            rent=data["rent"],
            bedrooms=data["bedrooms"],
            notes=data.get("notes", ""),
            commute_minutes=data.get("commute_minutes"),
        )

    def __repr__(self):
        return f"Apartment({self.name}, rent=₹{self.rent}, commute={self.commute_minutes}min)"



if __name__ == "__main__":
    test_apt = Apartment(
        name="Maple Court 2B",
        address="221 Maple St",
        rent=12000,
        bedrooms=1,
        commute_minutes=12,
    )
    print(test_apt)
    print("Score:", test_apt.score())