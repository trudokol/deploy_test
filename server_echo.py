import asyncio
import os
import logging
import json

HOST_IP = ""
PORT = 53333


async def handle_connection(reader, writer):
    address = writer.get_extra_info("peername")
    logging.info("Подключён: ", address)

    while True:
        try:
            data = await reader.read(4096)
            if not data:
                break

            logging.debug(data.decode())

            new_text = data.decode().upper() + "ADDITIONAL_TEXT1234"
            new_text = new_text.encode()
            writer.write(new_text)
            await writer.drain()
        except [KeyboardInterrupt, ConnectionError, ConnectionResetError]:
            logging.exception("Соединение оборвано")
            break

    logging.info("Отключён: ", address)
    writer.close()
    await writer.wait_closed()


def save_data(data):
    with open("data/datafile.json", 'w') as file:
        json.dump(data, file)


async def main():
    logging.basicConfig(level=logging.INFO, filename="py.log",
                        format="%(asctime)s %(levelname)s %(message)s")


    os.mkdir("data")
    save_data("Jopa")


    server = await asyncio.start_server(handle_connection, HOST_IP, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    logging.info(f'Serving on {addrs}')

    try:
        async with server:
            await server.serve_forever()

    except KeyboardInterrupt:
        server.close()    
    finally:
        logging.info("Сервер остановлен")




if __name__ == "__main__":
    asyncio.run(main())