from raph3 import raph as Raph
import asyncio

async def main():
    # Inicia el Sistema Raph3
    Raph.run()
    
    # Agrega la coorutina de ejecucion de tareas programadas
    schedule = asyncio.create_task(Raph.executeSchedule()) # ACTIVAR PARA ACCIONES  
 
    # Crea la rutina principal de ejecucion del servidor
    await Raph.app.run(host="0.0.0.0", port=80, debug=True, ssl=False )

    # Cancela la ejecucion de las tareas programadas
    await schedule.cancel()
    # Cierra el sistema
    Raph.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        Raph.stop()
    except Exception as e:
        print(e)
        Raph.stop()



