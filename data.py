'''''
import firebase_admin
from firebase import firebase

#cred= credentials.Certificate('./firstproject-efd33-firebase-adminsdk-ssqgd-6c39825d7b.json')
#defualt_app=firebase_admin.initialize_app(cred)

firebase=firebase.FirebaseApplication('https://firstproject-efd33.firebaseio.com/',None)

result=firebase.get('/firstproject-efd33:',None)
'''


from firebase import firebase

firebase=firebase.FirebaseApplication('https://carcontroller-76535.firebaseio.com/',None)

result=firebase.get('SteeringWheel',None)
control=firebase.put('SteeringWheel',str('forward'), '2' )
print(result)
