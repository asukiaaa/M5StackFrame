import cadquery as cq
from Helpers import show

baseXWidth = 50.0
baseYWidth = 50.0
baseHeight = 5.0
baseCornerR = 2.2
baseToOuterOffset = 2.0
baseToInnerOffset = 0
outerXWidth = baseXWidth + baseToOuterOffset * 2
outerYWidth = baseYWidth + baseToOuterOffset * 2
outerHeight = baseHeight
outerCornerR = baseCornerR + baseToOuterOffset
innerXWidth = baseXWidth + baseToInnerOffset * 2
innerYWidth = baseYWidth + baseToInnerOffset * 2
innerCornerR = baseCornerR + baseToInnerOffset
innerHeight = baseHeight*2
topHookXLengthFromBase = 5.0
topHookYLengthFromBase = 3.0
topHookHeight = 1.0
topHookOuterFromBase = 0.8
topHookXLength = topHookXLengthFromBase + topHookOuterFromBase
topHookYLength = topHookYLengthFromBase + topHookOuterFromBase
topHookCornerR = baseCornerR + topHookOuterFromBase
topHookSpaceXLength = topHookXLengthFromBase + baseToInnerOffset
topHookSpaceYLength = topHookYLengthFromBase + baseToInnerOffset
topHookSpaceCornerR = baseCornerR + baseToInnerOffset

case = cq.Workplane('XY').box(outerXWidth, outerYWidth, outerHeight) \
	.edges('|Z').fillet(outerCornerR) \
	.translate((0, 0, baseHeight/2))

innerSpace = cq.Workplane('XY').box(innerXWidth, innerYWidth, innerHeight) \
	.edges('|Z').fillet(innerCornerR) \
	.translate((0, 0, innerHeight/2))

topHook = cq.Workplane('XY').box(topHookXLength, topHookYLength, topHookHeight) \
	.edges('|Z and <X and <Y').fillet(topHookCornerR)

topHookSpace = cq.Workplane('XY').box(topHookSpaceXLength, topHookSpaceYLength ,topHookHeight) \
	.edges('|Z and <X and <Y').fillet(topHookSpaceCornerR) \
	.translate((
		(topHookXLength - topHookSpaceXLength) /2, \
		(topHookYLength - topHookSpaceYLength) /2, \
		0 \
	))

topHook.cut(topHookSpace)
topHook = topHook.translate(( \
		- innerXWidth/2 + topHookSpaceXLength / 2 - topHookOuterFromBase/2, \
		- innerYWidth/2 + topHookSpaceYLength / 2 - topHookOuterFromBase/2, \
		innerHeight/2 + topHookHeight/2, \
	))

show(topHook)

case.cut(innerSpace)

show(case)
