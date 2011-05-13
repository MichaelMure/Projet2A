import bge
from mathutils import Matrix


scene = bge.logic.getCurrentScene()
List = scene.objects
cont = bge.logic.getCurrentController()

aiguille = cont.owner
value = List['Quadri'].worldLinearVelocity.length


aiguille.localOrientation = Matrix.Rotation(-value / 10.0, 4, 'Z').to_3x3()