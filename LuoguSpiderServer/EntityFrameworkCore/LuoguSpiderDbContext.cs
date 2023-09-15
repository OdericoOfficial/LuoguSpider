using Microsoft.EntityFrameworkCore;

namespace LuoguSpiderServer.EntityFrameworkCore
{
    public class LuoguSpiderDbContext : DbContext
    {
        public LuoguSpiderDbContext(DbContextOptions<LuoguSpiderDbContext> options) : base(options)
        {

        }

        /// <summary>
        /// 由于没什么复杂的业务，所以就直接将DbContext放在本项目下方
        /// </summary>
        /// <param name="modelBuilder"></param>
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<LuoguProblem>()
                .HasKey(item => item.Id);
        }
    }
}
