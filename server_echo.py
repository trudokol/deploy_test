import asyncio

HOST_IP = ""
PORT = 53333


async def handle_connection(reader, writer):
    address = writer.get_extra_info("peername")
    print("Подключён: ", address)

    while True:
        try:
            data = await reader.read(4096)
            if not data:
                break

            print(data.decode())

            new_text = data.decode().upper() + "ADDITIONAL_TEXT1233"
            new_text = new_text.encode()
            writer.write(new_text)
            await writer.drain()
        except [KeyboardInterrupt, ConnectionError, ConnectionResetError]:
            break

    print("Отключён: ", address)
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_connection, HOST_IP, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    try:
        async with server:
            await server.serve_forever()

    except KeyboardInterrupt:
        print("Остановка...")
        server.close()    
    finally:
        print("Сервер остановлен")




if __name__ == "__main__":
    asyncio.run(main())