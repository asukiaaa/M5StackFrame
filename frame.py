import cadquery as cq

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
bottomSpaceHeightOffset = 0.5
bottomSpaceLengthOffset = 0.5
bottomSpaceWidthOffset = 0.3
bottomSpaceWidthFromBase = topHookOuterFromBase + bottomSpaceWidthOffset
bottomSpaceHeight = topHookHeight + bottomSpaceHeightOffset
bottomSpaceXLengthFromBase = topHookXLengthFromBase + bottomSpaceLengthOffset
bottomSpaceYLengthFromBase = topHookYLengthFromBase + bottomSpaceLengthOffset
bottomSpaceXLength = bottomSpaceXLengthFromBase + bottomSpaceWidthFromBase
bottomSpaceYLength = bottomSpaceYLengthFromBase + bottomSpaceWidthFromBase
bottomSpaceCornerR = topHookCornerR + bottomSpaceWidthOffset
screwHoleXFromBase = 10.0
screwHoleYFromBase = 3.0
screwHoleZFromBase = 0.0
screwHoleR = 2.0 / 2
screwHoleMountR = 5.0 / 2
screwHoleMountHeight = 2.0

case = cq.Workplane('XY').box(outerXWidth, outerYWidth, outerHeight) \
	.edges('|Z').fillet(outerCornerR) \
	.translate((0, 0, baseHeight/2))

innerSpace = cq.Workplane('XY').box(innerXWidth, innerYWidth, innerHeight) \
	.edges('|Z').fillet(innerCornerR) \
	.translate((0, 0, innerHeight/2))
case.cut(innerSpace)

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
		innerHeight/2 + topHookHeight/2))
case = case \
	.union(topHook) \
	.union(topHook.mirror(mirrorPlane='YZ')) \
	.union(topHook.mirror(mirrorPlane='XZ')) \
	.union(topHook.mirror(mirrorPlane='XZ').mirror(mirrorPlane='YZ'))

bottomSpace = cq.Workplane('XY').box(bottomSpaceXLength, bottomSpaceYLength, bottomSpaceHeight) \
	.edges('|Z and <X and <Y').fillet(bottomSpaceCornerR) \
	.translate((
		- innerXWidth / 2 + bottomSpaceXLength / 2 - bottomSpaceWidthFromBase,
		- innerYWidth / 2 + bottomSpaceYLength / 2 - bottomSpaceWidthFromBase,
		bottomSpaceHeight / 2))
case.cut(bottomSpace)
case.cut(bottomSpace.mirror(mirrorPlane='YZ'))
case.cut(bottomSpace.mirror(mirrorPlane='XZ'))
case.cut(bottomSpace.mirror(mirrorPlane='XZ').mirror(mirrorPlane='YZ'))

screwHoleXFromBase = 10.0
screwHoleYFromBase = 3.0
screwHoleR = 2.0 / 2
screwHoleMountR = 5.0 / 2
screwHoleHeight = 2.0

screwHole = cq.Workplane('XY').circle(screwHoleR).extrude(screwHoleMountHeight)
screwHoleMountBox = cq.Workplane('XY').box(screwHoleMountR * 2, screwHoleYFromBase, screwHoleMountHeight) \
	.translate((0, screwHoleYFromBase / 2, screwHoleMountHeight / 2))
screwHoleMount = cq.Workplane('XY').circle(screwHoleMountR).extrude(screwHoleMountHeight) \
	.union(screwHoleMountBox) \
	.cut(screwHole) \
	.translate((
		innerXWidth / 2 - screwHoleXFromBase,
		innerYWidth / 2 - screwHoleYFromBase,
		outerHeight - screwHoleMountHeight - screwHoleZFromBase))
case = case \
	.union(screwHoleMount) \
	.union(screwHoleMount.mirror(mirrorPlane='YZ')) \
	.union(screwHoleMount.mirror(mirrorPlane='XZ')) \
	.union(screwHoleMount.mirror(mirrorPlane='XZ').mirror(mirrorPlane='YZ'))

show_object(case, options={'rgba': (204, 204, 204, 0.4)})
