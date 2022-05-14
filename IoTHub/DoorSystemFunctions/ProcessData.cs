using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Azure.EventHubs;
using Microsoft.Azure.WebJobs;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace DoorSystemFunctions
{
    public static class ProcessData
    {
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
                    
                    SqlConnection con = new SqlConnection("Server=tcp:crhisjairo-iot-database-server.database.windows.net,1433;Initial Catalog=IoTDatabase;Persist Security Info=False;User ID=crhisjairo;Password=Cores2001;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;");
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
    }
}
