
var utils = require('../../js/competition-utils.js');

describe("The league sorter", function() {
	it("should be defined", function() {
		expect(utils.league_sorter).toBeDefined();
	});
	it("should sort inputs by points when already in order", function() {
		var raw = { 'ABC': 12.0, 'DEF': 3.5 };
		var expected = [
			{ 'tla': 'ABC', 'pos': 1, 'points': 12 },
			{ 'tla': 'DEF', 'pos': 2, 'points': 3.5 },
		];
		var league = utils.league_sorter(raw);
		expect(league).toEqual(expected);
	});
	it("should sort inputs by points when not already in order", function() {
		var raw = { 'ABC': 2.0, 'DEF': 3.5 };
		var expected = [
			{ 'tla': 'DEF', 'pos': 1, 'points': 3.5 },
			{ 'tla': 'ABC', 'pos': 2, 'points': 2 },
		];
		var league = utils.league_sorter(raw);
		expect(league).toEqual(expected);
	});
	it("should handle ties", function() {
		var raw = { 'ABC': 12.0, 'DEF': 5.0, 'GHI': 5.0, 'KLM': 2.0 };
		var expected = [
			{ 'tla': 'ABC', 'pos': 1, 'points': 12 },
			{ 'tla': 'DEF', 'pos': 2, 'points': 5 },
			{ 'tla': 'GHI', 'pos': '', 'points': 5 },
			{ 'tla': 'KLM', 'pos': 4, 'points': 2 },
		];
		var league = utils.league_sorter(raw);
		expect(league).toEqual(expected);
	});
	it("should be re-usable", function() {
		var raw_1 = { 'ABC': 12.0, 'DEF': 3.5 };
		var expected_1 = [
			{ 'tla': 'ABC', 'pos': 1, 'points': 12 },
			{ 'tla': 'DEF', 'pos': 2, 'points': 3.5 },
		];
		var raw_2 = { 'ABC': 2.0, 'DEF': 2.0 };
		var expected_2 = [
			{ 'tla': 'ABC', 'pos': 1, 'points': 2 },
			{ 'tla': 'DEF', 'pos': '', 'points': 2 },
		];
		var league_1 = utils.league_sorter(raw_1);
		expect(league_1).toEqual(expected_1);
		var league_2 = utils.league_sorter(raw_2);
		expect(league_2).toEqual(expected_2);
	});
	it("should include a cutoff row if there are enough teams", function() {
		var raw = { 'ABC': 12.0, 'DEF': 5.0 };
		var expected = [
			{ 'tla': 'ABC', 'pos': 1, 'points': 12 },
			{ 'tla': '-', 'pos': '-', 'points': '-' },
			{ 'tla': 'DEF', 'pos': 2, 'points': 5 },
		];
		var league = utils.league_sorter(raw, 1);
		expect(league).toEqual(expected);
	});
	it("should not include a cutoff row if there are few enough teams", function() {
		var raw = { 'ABC': 12.0, 'DEF': 5.0 };
		var expected = [
			{ 'tla': 'ABC', 'pos': 1, 'points': 12 },
			{ 'tla': 'DEF', 'pos': 2, 'points': 5 },
		];
		var league = utils.league_sorter(raw, 2);
		expect(league).toEqual(expected);
	});
});
