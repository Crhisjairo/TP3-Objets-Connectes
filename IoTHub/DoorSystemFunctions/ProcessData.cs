using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.EventHubs;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Microsoft.Azure.Devices;

namespace DoorSystemFunctions
{
    public static class ProcessData
    {
        static ServiceClient serviceClient;
        static string sqlConnectionString = "Server=tcp:crhisjairo-iot-database-server.database.windows.net,1433;Initial Catalog=IoTDatabase;Persist Security Info=False;User ID=crhisjairo;Password=Cores2001;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;";
        static string ioTHubConnectionString = "HostName=Crhisjairo-IoT.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=kxEfc8uAIV3uGJtSdgrwk/+bIGZgIM7rPTPg3cyzyXY=";
        static string targetDevice = "DoorSystemPi";

        [FunctionName("ProcessData")]
        public static async Task Run([EventHubTrigger("messages/events", Connection = "EventHubDefaultConnection")] EventData[] events, ILogger log)
        {
            var exceptions = new List<Exception>();

            foreach (EventData eventData in events)
            {
                try
                {
                    string messageBody = Encoding.UTF8.GetString(eventData.Body.Array, eventData.Body.Offset, eventData.Body.Count);
                    JObject systemDoorData = JObject.Parse(messageBody);

                    // Replace these two lines with your processing logic.
                    log.LogInformation($"C# Event Hub trigger function processed a message: {messageBody}");
                    
                    SqlConnection con = new SqlConnection(sqlConnectionString);
                    con.Open();

                    log.LogInformation(systemDoorData["DeviceId"].ToString());
                    log.LogInformation(systemDoorData["Temperature"].ToString());


                    String query = $"INSERT INTO dbo.DeviceInformation (DeviceID, Temperature, OpenDoorPercentage, Mode) " +
                                   $"VALUES ('{systemDoorData["DeviceId"]}', {systemDoorData["Temperature"]}, {systemDoorData["OpenDoorPercentage"]}, '{systemDoorData["Mode"]}');";
                    SqlCommand cmd = new SqlCommand(query, con);
                    cmd.ExecuteNonQuery();

                    await Task.Yield();
                }
                catch (Exception e)
                {
                    // We need to keep processing the rest of the batch - capture this exception and continue.
                    // Also, consider capturing details of the message that failed processing so it can be processed again later.
                    exceptions.Add(e);
                }
            }

            // Once processing of the batch is complete, if any messages in the batch failed processing throw an exception so that there is a record of the failure.

            if (exceptions.Count > 1)
                throw new AggregateException(exceptions);

            if (exceptions.Count == 1)
                throw exceptions.Single();
        }

        [FunctionName("GetData")]
        public static async Task<IActionResult> GetData([HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)] HttpRequestMessage req, TraceWriter log)
        {
            log.Info("GetData C# HTTP trigger function processed a request.");

            String query = "SELECT * FROM DeviceInformation;";

            DataTable table = new DataTable();
            SqlDataReader reader;

            using (SqlConnection con = new SqlConnection(sqlConnectionString))
            {
                con.Open();
                using (SqlCommand command = new SqlCommand(query, con))
                {
                    reader = command.ExecuteReader();

                    table.Load(reader);
                    reader.Close();
                    con.Close();
                }
            }


            return new OkObjectResult(new JsonResult(table));

            //return req.CreateResponse(HttpStatusCode.BadRequest, "Please pass a name on the query string or in the request body");
        }

        [FunctionName("SendMessage")]
        public static async Task<IActionResult> SendMessage([HttpTrigger(AuthorizationLevel.Function, "post", Route = null)] HttpRequestMessage req, TraceWriter log)
        {
            log.Info("Send Message C# HTTP trigger function processed a request.");

            serviceClient = ServiceClient.CreateFromConnectionString(ioTHubConnectionString);

            var content = req.Content;
            string jsonContent = content.ReadAsStringAsync().Result;
            log.Info(jsonContent);
            
            SendCloudToDeviceMessageAsync(jsonContent).Wait();

            return new OkObjectResult("{\"message\":\"Success\"}");
        }

        private async static Task SendCloudToDeviceMessageAsync(string jsonContent)
        {
            var commandMessage = new
             Message(Encoding.ASCII.GetBytes(jsonContent));
            await serviceClient.SendAsync(targetDevice, commandMessage);
        }
    }
}
