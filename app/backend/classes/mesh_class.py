from app.backend.db.models import MeshModel, EmployeeModel, MeshDetailModel, TurnModel
from sqlalchemy import desc, asc,extract, select
import json
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class MeshClass:
    def __init__(self, db):
        self.db = db
    def serialize_mesh(self, mesh):
        return {
            'turn': mesh.turn,
            'working': mesh.working,
            'start': str(mesh.start), 
            'end': str(mesh.end),
            'breaking': mesh.breaking,
            'group_day_id': mesh.group_day_id,
            'free_day_group_id': mesh.free_day_group_id,
            'total_week_hours': mesh.total_week_hours,
            'scheduled': f'{mesh.group_day_id} x {mesh.free_day_group_id}',
        }

    def get_turn_by_id(self, id):
        stmt = select(TurnModel.turn, TurnModel.working, TurnModel.start, TurnModel.end, TurnModel.breaking, TurnModel.group_day_id, TurnModel.free_day_group_id, TurnModel.total_week_hours).where(TurnModel.id == id)
        result = self.db.execute(stmt).first()
        print(result)
        return self.serialize_mesh(result)
        

    def group_by_week(self, data):
        grouped_data = {}
        for item in data:
            week_id = item['week_id']
            if week_id not in grouped_data:
                # Si la semana no está en el diccionario, la agregamos
                grouped_data[week_id] = item
                grouped_data[week_id]['date'] = [item['date']]

                # Obtener los datos del turno
                turn_data = self.get_turn_by_id(item['turn_id'])
                grouped_data[week_id]['turn_data'] = turn_data
            else:
                # Si la semana ya está en el diccionario, agregamos la fecha a la lista
                grouped_data[week_id]['date'].append(item['date'])

        return list(grouped_data.values())
    def getMeshByrutWeekPeriod(self, rut, period):
        try:
            periodYear = period.split('-')[0]
            periodMonth = period.split('-')[1]
            data = self.db.query(MeshDetailModel).filter(MeshDetailModel.rut == rut)\
                        .filter(extract('year', MeshDetailModel.date) == periodYear)\
                        .filter(extract('month', MeshDetailModel.date) == periodMonth).all()
            data = [item.__dict__ for item in data]  # Convertir los objetos a diccionarios
            grouped_data = self.group_by_week(data)
            return grouped_data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
   
    def get_all(self):
        try:
            data = self.db.query(MeshModel, EmployeeModel).outerjoin(EmployeeModel, MeshModel.rut == EmployeeModel.rut).order_by(desc(MeshModel.id)).all()
            return [row._asdict() for row in data]
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"

    
    def quantity_last_week_working_days(self, rut, year, month, dataLastWeek):
                data_dict = json.loads(dataLastWeek)
                try:
                    data = self.db.query(MeshModel)\
                        .filter(MeshModel.rut == rut)\
                        .filter(extract('year', MeshModel.date) == year)\
                        .filter(extract('month', MeshModel.date) == month)\
                        .filter(MeshModel.week_id == data_dict['week_id'] )\
                        .count()      
                    return data
                except Exception as e:
                    error_message = str(e)
                    return f"Error: {error_message}"
      
    def last_week_working_days(self, rut, year, month):
        try:
            data = self.db.query(MeshModel)\
                .filter(MeshModel.rut == rut)\
                .filter(extract('year', MeshModel.date) == year)\
                .filter(extract('month', MeshModel.date) == month)\
                .order_by(desc(MeshModel.week_id))\
                .first()      
            
            if data:
                # Serializar el objeto MeshModel a un diccionario
                mesh_data = {
                    'id': data.id,
                    'turn_id': data.turn_id,
                    'week_id': data.week_id,
                    'rut': data.rut,
                    'date': data.date.strftime("%Y-%m-%d"),
                    'added_date': data.added_date.strftime("%Y-%m-%d"),  # Convert the datetime object to a string format
                }

                # Convierte el diccionario a una cadena JSON
                serialized_data = json.dumps(mesh_data)

                return serialized_data
            else:
                return "No se encontraron datos para el campo especificado."

        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"

    def get(self, field, value):
        try:
            data = self.db.query(MeshModel).filter(getattr(MeshModel, field) == value).first()

            if data:
                # Serializar el objeto MeshModel a un diccionario
                mesh_data = {
                    'id': data.id,
                    'turn_id': data.turn_id,
                    'week_id': data.week_id,
                    'rut': data.rut,
                    'added_date': data.added_date.strftime("%Y-%m-%d"), 
                }


                # Convierte el diccionario a una cadena JSON
                serialized_data = json.dumps(mesh_data)

                return serialized_data

            else:
                return "No se encontraron datos para el campo especificado."

        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
  
    def store(self, inputs):
        try:
            # Crear la instancia de MeshModel solo si no existe una con el mismo rut y period
            first_date = datetime.fromisoformat(inputs['dates_in_range'][0])
            period = f"{first_date.year}-{first_date.month}"
            mesh_data = {key: inputs[key] for key in ('rut', 'added_date')}
            mesh_data['period'] = period

            mesh = self.db.query(MeshModel).filter_by(rut=mesh_data['rut'], period=mesh_data['period']).first()
            if not mesh:
                mesh = MeshModel(**mesh_data)
                self.db.add(mesh)
                self.db.commit()

            # Crear y guardar las instancias de MeshDetailModel
            for date in inputs['dates_in_range']:
                date_obj = datetime.fromisoformat(date)
                formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                detail_data = {
                    'week_id': inputs['week_id'],
                    'turn_id': inputs['turn_id'],
                    'mesh_id': mesh.id,
                    'rut': inputs['rut'],
                    'date': formatted_date,
                    'added_date': inputs['added_date'],
                }
                detail = MeshDetailModel(**detail_data)
                self.db.add(detail)

            self.db.commit()
            return 1
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"