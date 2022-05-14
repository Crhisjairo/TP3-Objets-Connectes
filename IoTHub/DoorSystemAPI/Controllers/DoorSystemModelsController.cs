using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using DoorSystemAPI.Models;
using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Configuration;
using System.Data;

namespace DoorSystemAPI.Controllers
{
    [Route("api/DoorSystemModels")]
    [ApiController]
    public class DoorSystemModelsController : ControllerBase
    {
        private readonly IConfiguration _configuration;

        public DoorSystemModelsController(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        // GET: api/DoorSystemModels
        [HttpGet]
        public JsonResult GetTodoItems()
        {
            String query = "SELECT * FROM DeviceInformation;";

            DataTable table = new DataTable();
            string sqlDataSource = _configuration.GetConnectionString("sqldb_connection");
            SqlDataReader reader;

            using (SqlConnection con = new SqlConnection(sqlDataSource))
            {
                con.Open();
                using(SqlCommand command = new SqlCommand(query, con))
                {
                    reader = command.ExecuteReader();

                    table.Load(reader);
                    reader.Close();
                    con.Close();
                }
            }

            return new JsonResult(table);
        }

        /*
        // GET: api/DoorSystemModels/5
        [HttpGet("{id}")]
        public async Task<ActionResult<DoorSystemModel>> GetDoorSystemModel(int id)
        {
            return null;
        }

        // PUT: api/DoorSystemModels/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutDoorSystemModel(int id, DoorSystemModel doorSystemModel)
        {
            if (id != doorSystemModel.Id)
            {
                return BadRequest();
            }

            _context.Entry(doorSystemModel).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!DoorSystemModelExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/DoorSystemModels
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<DoorSystemModel>> PostDoorSystemModel(DoorSystemModel doorSystemModel)
        {
            _context.DoorSystemModel.Add(doorSystemModel);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetDoorSystemModel", new { id = doorSystemModel.Id }, doorSystemModel);
        }

        // DELETE: api/DoorSystemModels/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteDoorSystemModel(int id)
        {
            var doorSystemModel = await _context.DoorSystemModel.FindAsync(id);
            if (doorSystemModel == null)
            {
                return NotFound();
            }

            _context.DoorSystemModel.Remove(doorSystemModel);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool DoorSystemModelExists(int id)
        {
            return _context.DoorSystemModel.Any(e => e.Id == id);
        }*/
    }
}
