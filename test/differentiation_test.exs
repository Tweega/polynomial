defmodule Sandbox.Differentiate.Test do
  use ExUnit.Case
  doctest Sandbox

  test "I can parse a slash separated string into a list" do
    assert Sandbox.Differentiate.parsePoly("1/2/3") == [1, 2, 3]
  end

  test "I can drop the final term" do
    assert Sandbox.Differentiate.dropFinalTerm([1, 2, 3]) == [1, 2]
  end

  # test "I can transform list into a polynomial expression " do
  #   assert Sandbox.Differentiate.translatePoly("1/2/3") == "x^2 + 2x + 3"
  # end

  test "I can map list to multiply coefficient by exponent -1 test 1 " do
    assert Sandbox.Differentiate.getDiffCoefficients([1, 2, 3]) == [2, 2]
  end


  test "I can map list to multiply coefficient by exponent -1 test 2" do
    assert Sandbox.Differentiate.getDiffCoefficients([3, 2, 1]) == [6, 2]
  end


  test "I can map list to multiply coefficient by exponent -1 test 3" do
    assert Sandbox.Differentiate.getDiffCoefficients([4, 3, 2, 1]) == [12, 6, 2]
  end


  test "I can create a differented polynomial expression test 1" do
    assert Sandbox.Differentiate.translatePoly("1/2/3") == "2x + 2"
  end


    test "I can create a differented polynomial expression test 2" do
      assert Sandbox.Differentiate.translatePoly("4/3/2/1") == "12x^2 + 6x + 2"
    end
end
