using Microsoft.EntityFrameworkCore;

namespace LuoguSpiderServer.EntityFrameworkCore
{
    public class LuoguSpiderDbContext : DbContext
    {
        public LuoguSpiderDbContext(DbContextOptions<LuoguSpiderDbContext> options) : base(options)
        {

        }
    }
}
