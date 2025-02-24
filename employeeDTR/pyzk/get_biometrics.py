from zk import ZK, const
import pytz
from datetime import datetime, timedelta
from django.utils import timezone
from employeeDTR.models import Employee, DTR


def capture_biometric():
    conn = None
    zk = ZK('192.168.1.201', port=4370, timeout=5, password=0, force_udp=True, ommit_ping=False)
    try:
        conn = zk.connect()
        conn.disable_device()

        device_timezone = 'Asia/Manila' 
        conn.set_time(datetime.now(pytz.timezone(device_timezone)))

        print("Please place your finger on the device...")
        for attendance in conn.live_capture():
            if attendance is None:
                # implement here timeout logic
                conn.end_live_capture = True
                capture_biometric()
                pass
            else:
                print('ATTENDANCE', attendance)
                user_id = attendance.user_id

                # Get employee by ID
                try:
                    today = datetime.today()
                    employee = Employee.objects.get(id=user_id)
                
                    print("Employee found")
                    print('ID:',employee.id)
                    print('NAME:',employee.first_name +" "+ employee.last_name)
                    print('EMPLOYEE TYPE:',employee.employee_type)

                    print('employee_ID:',employee.employee_id)
                    print('department:',employee.department)
 
                            # Get the most recent attendance record for today
                    today = timezone.now().date()
                    print('TODAY:', today)
                    emp_attendance = DTR.objects.filter(id_number=user_id, datetime__date=today).order_by('-datetime').first()
                    inOut = 'C/In'
                    if emp_attendance:
                        print('attendance:', emp_attendance)
                        print('attendance + 5 mins:', emp_attendance.datetime + timedelta(minutes=5))
                        print('attendance.timestamp:', attendance.timestamp)
                        last_timestamp=emp_attendance.datetime
                        # MINUTES OF INTERVAL  // IN & OUT
                        five_min_after_last=last_timestamp+timedelta(minutes=5)
                        current_timestamp=timezone.now()
                        
                        #inOut = 'C/Out' if emp_attendance.datetime + timedelta(minutes=5) < attendance.timestamp else 'C/In' 
                        
                        #if emp_attendance.datetime + timedelta(minutes=5) < current_timestamp:
                        #    inOut = 'C/Out' if emp_attendance.status == 'C/In' else 'C/Out' # 'C/In' Toggle between Cin Cout
                        #    print(f"Next Status: {inOut}")
                        if current_timestamp >= five_min_after_last:
                            inOut='C/Out' if emp_attendance.status == 'C/In' else 'C/In'
                        else:
                            inOut = emp_attendance.status
                        print(f"Next Status: {inOut}")
                        
                    else:
                        print(f"No attendance record found for employee with ID {user_id} on {today}")
         
                  
                    DTR.objects.create(
                        department=employee.department if employee else 'Unknown',
                        name=f"{employee.first_name} {employee.last_name}" if employee else 'Unknown',
                        number=employee.employee_id,
                        datetime=attendance.timestamp,
                        status=inOut,
                        location_id=1,  
                        id_number=attendance.user_id,
                    )
                    print("Attendance data saved to the DTR model.")


                except Employee.DoesNotExist:
                    print(f"No employee found with ID {user_id}")


    except Exception as e:
        print("Process failed: {}".format(e))
    finally:
        if conn:
            conn.enable_device()
            conn.disconnect()

if __name__ == "__main__":
    capture_biometric()