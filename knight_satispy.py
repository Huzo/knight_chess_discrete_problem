from satispy import Variable, Cnf
from satispy.solver import Minisat


def knight(N=8):
	white_knight_at = [[Variable("W_{" + str(i) + str(j) + "}") for i in range(N)] for j in range(N)]
	black_knight_at = [[Variable("B_{" + str(i) + str(j) + "}") for i in range(N)] for j in range(N)]

	formula = Cnf()  # the overall formula

	# at least one black and white knight in each row
	for i in range(N):
		oneinthisrow_w = Cnf()
		oneinthisrow_b = Cnf()
		for j in range(N):
			oneinthisrow_w |= white_knight_at[i][j]
			oneinthisrow_b |= black_knight_at[i][j]
		formula &= (oneinthisrow_w & oneinthisrow_b)

	# at least one black and white knight in each column
	for j in range(N):
		oneinthiscolumn_w = Cnf()
		oneinthiscolumn_b = Cnf()
		for i in range(N):
			oneinthiscolumn_w |= white_knight_at[i][j]
			oneinthiscolumn_b |= black_knight_at[i][j] & (-white_knight_at[i][j])
		formula &= (oneinthiscolumn_w & oneinthiscolumn_b)

	# Each row and column has exactly 1 black and white knight
	for i1 in range(N):
		for j1 in range(N):
			for i2 in range(N):
				for j2 in range(N):
					if N * i1 + j1 < N * i2 + j2:  # Eliminate mirrors
						if(i1 == i2) | (j1 == j2):  # If two possible placements share the same row or column
							formula &= ((-white_knight_at[i1][j1]) | (-white_knight_at[i2][j2])) & ((-black_knight_at[i1][j1]) | (-black_knight_at[i2][j2]))

	# Can't attack same color
	for i1 in range(N):
		for j1 in range(N):
			for i2 in range(N):
				for j2 in range(N):
					if N * i1 + j1 < N * i2 + j2:  # Eliminate mirrors
						if((i1 - i2)**2 + (j1 - j2)**2 == 5) & ((i1 - i2 <= 2) & (j1 - j2 <= 2)):  # "L" shape attack
							formula &= ((-white_knight_at[i1][j1]) | (-white_knight_at[i2][j2])) & ((-black_knight_at[i1][j1]) | (-black_knight_at[i2][j2]))

	# White must attack at least one enemy
	for i1 in range(N):
		for j1 in range(N):
			white_must_attack_one = Cnf()
			for i2 in range(N):
				for j2 in range(N):
					if((i1 - i2)**2 + (j1 - j2)**2 == 5) & ((i1 - i2 <= 2) & (j1 - j2 <= 2)):  # "L" shape attack
						white_must_attack_one |= (white_knight_at[i1][j1]) & (black_knight_at[i2][j2])
			formula &= (white_knight_at[i1][j1] >> white_must_attack_one)

	# Black must attack at least one enemy
	for i1 in range(N):
		for j1 in range(N):
			black_must_attack_one = Cnf()
			for i2 in range(N):
				for j2 in range(N):
					if((i1 - i2)**2 + (j1 - j2)**2 == 5) & ((i1 - i2 <= 2) & (j1 - j2 <= 2)):  # "L" shape attack
						black_must_attack_one |= (black_knight_at[i1][j1]) & (white_knight_at[i2][j2])
			formula &= (black_knight_at[i1][j1] >> black_must_attack_one)

	solution = Minisat().solve(formula)

	if solution.error is True:
		print("Error: " + solution.error)
	elif solution.success:
		chessboard = ""
		for i in range(N):
			for j in range(N):
				if solution[white_knight_at[i][j]]:
					chessboard += "1"
				elif solution[black_knight_at[i][j]]:
					chessboard += "2"
				else:
					chessboard += "0"
			chessboard += "\n"
		print(chessboard)
	else:
		print("No valid solution")


if __name__ == '__main__':
	for i in range(1, 11):
		print(str(i) + "X" + str(i) + "board:")
		knight(i)
		print("\n\n")
