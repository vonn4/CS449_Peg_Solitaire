"""Determine the player's rating from the final number of pegs."""


class RatingPolicy:
    """Apply the rating thresholds suggested by the project overview."""

    def rate(self, remaining_pegs: int) -> str:
        """Return a rating for a completed game's positive peg count.

        Args:
            remaining_pegs: Number of pegs left when play ends.

        Returns:
            Outstanding, Very Good, Good, or Average.

        Raises:
            TypeError: If remaining_pegs is not an integer or is a boolean.
            ValueError: If remaining_pegs is less than one.
        """
        if isinstance(remaining_pegs, bool) or not isinstance(
            remaining_pegs, int
        ):
            raise TypeError("remaining_pegs must be an integer.")

        if remaining_pegs < 1:
            raise ValueError("remaining_pegs must be at least one.")

        if remaining_pegs == 1:
            return "Outstanding"
        if remaining_pegs == 2:
            return "Very Good"
        if remaining_pegs == 3:
            return "Good"
        return "Average"