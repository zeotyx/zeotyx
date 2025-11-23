using ConsolePlot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;

namespace algoritm
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;
            Console.Write("Enter launch angle (°): ");
            double angle = Convert.ToDouble(Console.ReadLine());
            Console.Write("Enter initial speed (m/s): ");
            double speed = Convert.ToDouble(Console.ReadLine());
            Console.Write("Enter starting height (m): ");
            double height = Convert.ToDouble(Console.ReadLine());
            projectile(angle, speed, height);
            
            
        }
        static void projectile(double launch_angle,double initial_speed, double starting_height)
        {
            float g_const = 9.81f;

            double rad = launch_angle * Math.PI / 180;
            double vx = initial_speed * Math.Cos(rad);
            double vy = initial_speed * Math.Sin(rad);

            double tPeak = vy / g_const;
            double totalTime = TotalTime(g_const, vy, starting_height);
            double ymax = starting_height + vy * tPeak - 0.5 * g_const * tPeak * tPeak;
            double X_range = vx * totalTime;

            Console.WriteLine($"Horizontal vel: {vx} m/s");
            Console.WriteLine($"Vertical vel: {vy} m/s");
            Console.WriteLine($"Time to peak: {tPeak}s, Total time: {totalTime}s");
            Console.WriteLine($"Max height: {ymax} m, Range: {X_range} m\n");


            int steps = 200;
            List<double> xD = new List<double>();
            List<double> yD = new List<double>();
            for (int i = 0; i <= steps; i++)
            {
                
                double t = totalTime * i / steps;
                double x = vx * t;
                double y = starting_height + vy * t - 0.5 * g_const * t * t;
                if (y < 0) y = 0;
                xD.Add(x);
                yD.Add(y);
            }


            double maxY = yD.Max();
            if (maxY < 0.5) maxY = 0.5;
            double maxX = xD.Max();
            double scaleX = 100;
            double scaleY = Math.Max(20, 20 * maxY / maxX); 
            double[] xNorm = xD.Select(x => x / maxX * scaleX).ToArray();
            double[] yNorm = yD.Select(y => y / maxY * scaleY).ToArray();

            var plt = new Plot(width: 100, height: 20);
            plt.AddSeries(xNorm, yNorm);
            plt.Draw();
            plt.Render();
        }
        static double TotalTime(float g_const, double vy, double starting_height)
        {
            if (starting_height == 0)
            {
                return 2 * vy / g_const;
            }
            double a = -0.5 * g_const;
            double b = vy;
            double c = starting_height;
            double discriminant = b * b - 4 * a * c;
            double t1 = (-b + Math.Sqrt(discriminant)) / (2 * a);
            double t2 = (-b - Math.Sqrt(discriminant)) / (2 * a);
            return Math.Max(t1, t2);
        }

    }
}
