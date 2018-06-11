from flask import Flask
from flask_restplus import Api, Resource, fields


app = Flask(__name__)

api = Api(
   app, 
   version='1.0', 
   title='Policy Recommendation API',
   description='Segregating policy based on consumer behaviour')

ns = api.namespace('namespace_tim', 
   description='')

resource_fields = api.model('Resource', {
    'result': fields.String,
})

# order_count
# isFirstBulk
# linked_to
# no_of_phones_associated
# no_of_address_associated
# promotion

parser = api.parser()
parser.add_argument(
   'State', 
   # type=float, 
   required=True, 
   location='form')

parser.add_argument(
   'Coverage', 
   #type=float, 
   required=True, 
   location='form')

parser.add_argument(
   'Education', 
   #type=float, 
   required=True, 
   location='form')

parser.add_argument(
   'Gender', 
   #type=float, 
   required=True, 
   location='form')

parser.add_argument(
   'Income', 
   type=float, 
   required=True, 
   location='form')

parser.add_argument(
   'Location_Code', 
   #type=float, 
   required=True, 
   location='form')

parser.add_argument(
   'Marital_Status', 
   #type=float, 
   required=True, 
   location='form')

parser.add_argument(
   'Sales_Channel', 
   #type=float, 
   required=True, 
   location='form')

parser.add_argument(
   'Vehicle_Class', 
   #type=float, 
   required=True, 
   location='form')

parser.add_argument(
   'Vehicle_Size', 
   #type=float, 
   required=True, 
   location='form')



@ns.route('/')
class CreditApi(Resource):

   @api.doc(parser=parser)
   @api.marshal_with(resource_fields)
   def post(self):
     args = parser.parse_args()
     result = self.get_result(args)

     return result, 201

   def get_result(self, args):
      State = args["State"]
      Coverage = args["Coverage"]
      Education = args["Education"]
      Gender = args["Gender"]
      Income = args["Income"]
      Location_Code = args["Location_Code"]
      Marital_Status = args["Marital_Status"]
      Sales_Channel = args["Sales_Channel"]
      Vehicle_Class = args["Vehicle_Class"]
      Vehicle_Size = args["Vehicle_Size"]
   

      from pandas import DataFrame
      df = DataFrame([[
         State,
         Coverage,
         Education,
         Gender,
         Income,
         Location_Code,
         Marital_Status,
         Sales_Channel,
         Vehicle_Class,
         Vehicle_Size
      ]])

      from sklearn.externals import joblib
      clf = joblib.load('model/nb.pkl');

      result = clf.predict(df)
      if(result[0] == 1.0): 
         result = "Trader" 
      else: 
         result = "Not a trader"

      return {
         "result": result
      }

if __name__ == '__main__':
    app.run(debug=True)
