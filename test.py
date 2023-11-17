import struct
import hashlib


def sender(conn, msg: bytes):

    pack_head = struct.pack('i', len(msg))
    conn.send(pack_head)
    conn.send(msg)


def receiver(conn) -> str:
    length = struct.unpack('i', conn.recv(4))[0]
    msg = ''
    while True:
        if length < 1024:
            recv_msg = conn.recv(length)
            msg += recv_msg.decode('utf-8')
            break
        else:
            recv_msg = conn.recv(1024)
            length -= 1024
            msg = recv_msg.decode('utf-8')

    return msg


class HashCheck:
    def __init__(self):
        self.md5 = hashlib.sha3_256()

    def hash_md5(self, msg: bytes):
        self.md5.update(msg)












# send side
def send_file(conn,filename):

    # 获取文件大小
    size = os.path.getsize(filename)
    # 发送文件大小
    test.sender(conn, str(size).encode('utf-8'))

    with open(filename, 'rb') as f:
        # 创建md5 的验证对象
        md5obj = test.HashCheck()
        for line in f:
            # 追加MD5 验证
            md5obj.hash_md5(line)
            # 发送文件行
            test.sender(conn, line)
    test.sender(conn, md5obj.md5.hexdigest().encode('utf-8'))



# receive side
def recv_file(c, filename):
    md5obj = proto.HashCheck()
    with open(filename, 'w') as f:
        """
        1. 获取文件大小
        2. 循环获取文件行
        3. 追加验证文件完整性，并将文件行内容写入文件
        4. 文件读完后 获取文件的MD5
        5. 将获取的MD5与 计算的MD5 进行比较。
        """

        size = proto.receiver(c)
        file_size = int(size)
        while True:
            try:
                line = proto.receiver(c)
                md5obj.hash_md5(line.encode('utf-8'))
                f.write(line)
                file_size -= len(line)

                #  文件接收完成
                if file_size == 0:
                    break

            except Exception as e:
                print('连接异常')
                c.close()
                print(traceback.print_exc())
                break
        hash_md5 = proto.receiver(c)
        if hash_md5 == md5obj.md5.hexdigest():
            print('file receive success!')
        else:
            print('file receive failed!')