import A
if __name__ == "__main__":
	
	start = A.Node([[4,5,7],[0,2,3],[1,6,8]])
	end = A.Node([[1,2,3],[4,0,5],[6,7,8]])

	a = A.A(start, end)

	if a.start():
		a.labelPath()
		a.saveTree()
	else:
		print("Fail")