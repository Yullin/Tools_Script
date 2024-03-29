func GetAllLocalIP() {
    addrs, err := net.InterfaceAddrs()
    if err != nil {
        fmt.Println(err)
        return
    }
    for _, address := range addrs {
        // 检查ip地址判断是否回环地址
        if ipnet, ok := address.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
            if ipnet.IP.To4() != nil {
                fmt.Println(ipnet.IP.String())
            }
        }
    }
}

func GetOutBoundIP()(ip string, err error)  {
    conn, err := net.Dial("udp", "8.8.8.8:53")
    if err != nil {
        fmt.Println(err)
        return
    }
    localAddr := conn.LocalAddr().(*net.UDPAddr)
    fmt.Println(localAddr.String())
    ip = strings.Split(localAddr.String(), ":")[0]
    return
}
func main() {
    ip, err := GetOutBoundIP()
    if err != nil {
        fmt.Println(err)
    }
    fmt.Println(ip)
}
