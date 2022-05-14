using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace DoorSystemAPI.Models
{
    public class DoorSystemModelContext: DbContext
    {
        public DoorSystemModelContext(DbContextOptions<DoorSystemModelContext> options)
            : base(options)
        {
        }

        public DbSet<DoorSystemModel> DoorSystemModel { get; set; } = null!;

    }
}
