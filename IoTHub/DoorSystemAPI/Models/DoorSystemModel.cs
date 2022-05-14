using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace DoorSystemAPI.Models
{
    public class DoorSystemModel
    {
        [Key]
        public int Id { get; set; }
        public string DeviceId { get; set; }
        public string Temperature { get; set; }
        public string OpenDoorPercentage { get; set; }
        public string Mode { get; set; }
    }
}
