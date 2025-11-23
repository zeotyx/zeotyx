using System;

namespace NeuralNetwork
{
    internal class Program
    {
        static void Main(string[] args)
        {
            while (true)
            {
                Console.Clear();                
                int choice = Convert.ToInt32(ReadFloat("Peptide GUI\n1)Peptide calculater\n2)\n3)\n4)\n"));
                if (choice == 1)
                {
                    int choice1 = Convert.ToInt32(ReadFloat("Peptide Calculator\n1)Peptide units\n2)DosetoVolumeConvertor\n3)Reconstitution Calculator\n4)\n"));
                     if(choice1 == 1)
                    {
                        Console.Clear();
                        float mg = ReadFloat("How many mg of peptide do you have? ");
                        float ml = ReadFloat("How much BAC water (ml) do you have? ");
                        float mcg = ReadFloat("What concentration do you want (mcg/ml)? ");


                        string units = BacCalc(mcg, mg, ml, string.Empty);
                        Console.Clear();
                        Console.WriteLine("\n--- Results ---");
                        Console.WriteLine($"Total peptide: {mg * 1000} mcg" +
                            $"\nFinal concentration: {mcg} mcg per ml" +
                            $"\nUnits per injection: {units}" +
                            $"\n     press any key to go back to main menu");
                        Console.ReadKey();
                    }
                    if (choice1 == 2)
                    {
                        Console.Clear();
                        float mcg = ReadFloat("how much do you want to inject(mcg)? ");
                        float concentration = ReadFloat("What concentration do you have (mcg/ml)? ");
                        Console.WriteLine($"ml to inject: {DoseToVolume(mcg,concentration )}ml" +
                            $"\n     press any key to go back to main menu");
                        Console.ReadKey();

                    }
                    if(choice1 == 3)
                    {
                        Console.Clear();
                        float mg = ReadFloat("how much mg of peptide do you have? ");
                        float concentration = ReadFloat("What concentration do you want to achieve (mcg/ml)? ");
                        Console.WriteLine($"ADD: {BacHelper(mg, concentration)}ml of baC" +
                            $"\n     press any key to go back to main menu");
                        Console.ReadKey();
                    }
                }
            }            

        }
        static float ReadFloat(string prompt)
        {
            float value;
            Console.Write(prompt);
            while (!float.TryParse(Console.ReadLine(), out value) || value <= 0)
            {
                Console.Write("Invalid input, try again: ");
            }
            return value;
        }

        static float DoseToVolume(float doseMcg, float concentration) => doseMcg / concentration;
        static float BacHelper(float peptide_mg, float target_concentration) => (peptide_mg * 1000) / target_concentration;
        static string BacCalc(float concetration, float peptide_mg, float water_ml,string units) =>  units = ((concetration / ((peptide_mg *1000) / water_ml)) * 100).ToString();
        
    }

    
}
