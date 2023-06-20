using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
using UnityEngine.Experimental.GlobalIllumination;
using UnityEngine.UIElements;

public class socket_practice : MonoBehaviour
{
    public Rigidbody rb;
    Thread thread;
    public int connectionPort = 25001;
    TcpListener server;
    TcpClient client;
    bool running;


    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        ThreadStart ts = new ThreadStart(GetData);
        thread = new Thread(ts);
        thread.Start();
    }

    // Update is called once per frame
    void GetData()
    {
        server = new TcpListener(IPAddress.Any, connectionPort);
        server.Start();

        client = server.AcceptTcpClient();

        running = true;

        while (running)
        {
            Connection();
        }

        server.Stop();
    }

    void Connection()
    {
        NetworkStream nwStream = client.GetStream();

        byte[] buffer = new byte[client.ReceiveBufferSize];
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize);

        string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead);

        if (dataReceived != null && dataReceived != "")
        {
            //velocity = transform.InverseTransformDirection(rb.velocity);
            velocity = ParseData1(dataReceived);
            //angular = transform.InverseTransformDirection(rb.angularVelocity);
            angular = ParseData2(dataReceived);

            nwStream.Write(buffer, 0, bytesRead);
        }
    }

    public static Vector3 ParseData1(string dataString)
    {
        Debug.Log(dataString);

        if (dataString.StartsWith("(") && dataString.EndsWith(")"))
        {
            dataString = dataString.Substring(1, dataString.Length - 2);
        }

        string[] stringArray = dataString.Split(',');

        // Vector3 result = new Vector3(float.Parse(stringArray[0]), float.Parse(stringArray[1]), float.Parse(stringArray[2]));
        Vector3 result = new Vector3(float.Parse(stringArray[0]), 0, -float.Parse(stringArray[1]));

        return result;
    }

    public static Vector3 ParseData2(string dataString)
    {
        Debug.Log(dataString);

        if (dataString.StartsWith("(") && dataString.EndsWith(")"))
        {
            dataString = dataString.Substring(1, dataString.Length - 2);
        }

        string[] stringArray = dataString.Split(',');

        // Vector3 result = new Vector3(float.Parse(stringArray[0]), float.Parse(stringArray[1]), float.Parse(stringArray[2]));
        Vector3 result = new Vector3(0, float.Parse(stringArray[2]), 0);

        return result;
    }

    Vector3 velocity = Vector3.zero;
    Vector3 angular = Vector3.zero;

    private void Update()
    {
        //transform.position = velocity;
        //transform.rotation = Quaternion.Euler(angular);
        rb.velocity = transform.TransformDirection(velocity);
        rb.angularVelocity = transform.TransformDirection(angular);
    }
}
